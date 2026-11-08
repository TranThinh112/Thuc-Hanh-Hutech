"""
Module quét và phân tích chứng thư SSL/TLS của CertGuard.

Mọi kết quả đều được lấy TRỰC TIẾP từ quá trình bắt tay TLS với máy chủ đích,
không có dữ liệu nào được nhập sẵn.

Luồng xử lý của scan():
    1. Chuẩn hóa và kiểm tra đầu vào (hostname, cổng)
    2. Phân giải DNS + chống SSRF (chặn IP nội bộ, trừ khi nằm trong danh sách cho phép)
    3. Bắt tay TLS, lấy chuỗi chứng thư máy chủ gửi về
    4. Phân tích chứng thư lá (leaf): thời hạn, hostname, khóa, thuật toán ký
    5. Kiểm tra chuỗi tin cậy (dùng bộ xác thực X.509 của thư viện cryptography)
    6. Kiểm tra cấu hình TLS: phiên bản giao thức, cipher yếu, HSTS
    7. Kiểm tra thu hồi (OCSP / CRL) nếu chứng thư có khai báo
    8. Chấm điểm A+ ... F
"""
from __future__ import annotations

import datetime as dt
import fnmatch
import ipaddress
import re
import select
import socket
import ssl
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

import certifi
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dsa, ec, ed448, ed25519, rsa
from cryptography.x509 import ocsp
from cryptography.x509.oid import ExtensionOID, NameOID
from cryptography.x509.verification import PolicyBuilder, Store, VerificationError

UTC = dt.timezone.utc
HOST_RE = re.compile(r"^(?=.{1,253}$)([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*"
                     r"[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$")

# Mức độ nghiêm trọng của từng phát hiện
CRITICAL, HIGH, MEDIUM, LOW, INFO = "critical", "high", "medium", "low", "info"
GRADES = ["A+", "A", "B", "C", "D", "E", "F"]


class ScanError(Exception):
    """Lỗi khiến không thể quét (đầu vào sai, bị chặn SSRF, không kết nối được...)."""


class BlockedTarget(ScanError):
    """Mục tiêu bị chặn bởi cơ chế chống SSRF."""


@dataclass
class Finding:
    code: str
    severity: str
    message: str
    cap: str | None = None  # Điểm tối đa nếu gặp lỗi này


@dataclass
class ScanOptions:
    timeout: float = 6.0
    allowlist: list[str] = field(default_factory=list)  # vd: ["*.certguard.webservers"]
    extra_roots_dir: Path | None = None
    warn_days: int = 30
    critical_days: int = 7
    check_revocation: bool = True


# ---------------------------------------------------------------------------
# 1-2. Đầu vào và chống SSRF
# ---------------------------------------------------------------------------
def normalize_target(text: str, default_port: int = 443) -> tuple[str, int]:
    """Nhận 'example.com', 'example.com:8443' hoặc 'https://example.com:8443/abc'."""
    text = (text or "").strip()
    if not text:
        raise ScanError("Chưa nhập tên miền")
    if "://" not in text:
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:(?!\d)", text):
            raise ScanError("Chỉ hỗ trợ địa chỉ dạng tên miền hoặc https://")
        text = "https://" + text
    try:
        u = urlparse(text)
        host = (u.hostname or "").lower().rstrip(".")
        port = u.port or default_port
    except ValueError as e:
        raise ScanError(f"Địa chỉ không hợp lệ: {e}") from None
    if u.scheme not in ("https", "http"):
        raise ScanError("Chỉ hỗ trợ địa chỉ dạng tên miền hoặc https://")
    if not (1 <= port <= 65535):
        raise ScanError("Cổng phải nằm trong khoảng 1-65535")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if not HOST_RE.match(host):
            raise ScanError("Tên miền không hợp lệ") from None
    return host, port


def host_allowed(host: str, allowlist: list[str]) -> bool:
    return any(fnmatch.fnmatch(host, pat.strip().lower()) for pat in allowlist if pat.strip())


def resolve_safe(host: str, port: int, allowlist: list[str]) -> str:
    """
    Phân giải DNS và chặn SSRF.

    Kẻ tấn công có thể nhập 127.0.0.1, 192.168.x.x, 169.254.169.254 (metadata cloud)...
    để biến công cụ quét thành bàn đạp dò quét mạng nội bộ. Vì vậy mọi IP không phải
    IP công cộng (is_global=False) đều bị chặn, trừ tên miền nằm trong allowlist do
    quản trị viên cấu hình. Ta trả về IP đã kiểm tra và kết nối thẳng tới IP đó để
    tránh tấn công DNS rebinding (DNS trả IP khác ở lần phân giải thứ hai).
    """
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except socket.gaierror:
        raise ScanError(f"Không phân giải được tên miền '{host}'") from None
    ips = list(dict.fromkeys(i[4][0] for i in infos))
    internal = [ip for ip in ips if not ipaddress.ip_address(ip).is_global]
    if internal and not host_allowed(host, allowlist):
        raise BlockedTarget(
            f"Đã chặn: '{host}' trỏ tới địa chỉ nội bộ {', '.join(internal)} (chống SSRF). "
            "Quản trị viên có thể thêm tên miền vào danh sách cho phép nếu đây là máy chủ nội bộ hợp lệ.")
    # Ưu tiên IPv4 cho ổn định
    ips.sort(key=lambda ip: ":" in ip)
    return ips[0]


def check_url_safe(url: str, allowlist: list[str]) -> None:
    """URL OCSP/CRL nằm TRONG chứng thư do máy chủ gửi (dữ liệu không tin cậy) nên cũng phải kiểm tra SSRF."""
    u = urlparse(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise BlockedTarget("URL không hợp lệ")
    resolve_safe(u.hostname, u.port or (443 if u.scheme == "https" else 80), allowlist)


# ---------------------------------------------------------------------------
# 3. Bắt tay TLS
# ---------------------------------------------------------------------------
def _client_context(min_v=None, max_v=None, ciphers="DEFAULT:@SECLEVEL=0") -> ssl.SSLContext:
    """Context KHÔNG xác thực: ta muốn nhận cả chứng thư lỗi để phân tích, việc xác thực làm riêng."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.set_ciphers(ciphers)
    if min_v:
        ctx.minimum_version = min_v
    if max_v:
        ctx.maximum_version = max_v
    return ctx


def fetch_chain(ip: str, port: int, sni: str, timeout: float):
    """Trả về (danh sách chứng thư theo thứ tự máy chủ gửi, phiên bản TLS, cipher)."""
    sni_name = None if _is_ip(sni) else sni
    try:
        sock = socket.create_connection((ip, port), timeout=timeout)
    except OSError as e:
        raise ScanError(f"Không kết nối được tới {sni}:{port} ({e.strerror or e})") from None

    if hasattr(ssl.SSLSocket, "get_unverified_chain"):  # Python 3.13+
        try:
            with _client_context().wrap_socket(sock, server_hostname=sni_name) as s:
                raw = s.get_unverified_chain() or []
                ders = [c if isinstance(c, bytes) else c.public_bytes(1) for c in raw]
                version, cipher = s.version(), s.cipher()
        except (ssl.SSLError, OSError) as e:
            raise ScanError(f"Bắt tay TLS thất bại: {e}") from None
        certs = [x509.load_der_x509_certificate(d) for d in ders]
        return certs, version, cipher[0] if cipher else None

    # Python < 3.13: dùng pyOpenSSL để lấy được toàn bộ chuỗi
    from OpenSSL import SSL
    try:
        ctx = SSL.Context(SSL.TLS_CLIENT_METHOD)
        ctx.set_cipher_list(b"DEFAULT:@SECLEVEL=0")
        conn = SSL.Connection(ctx, sock)
        if sni_name:
            conn.set_tlsext_host_name(sni_name.encode())
        conn.set_connect_state()
        # Socket có timeout -> pyOpenSSL chạy ở chế độ không chặn, phải tự chờ dữ liệu
        while True:
            try:
                conn.do_handshake()
                break
            except SSL.WantReadError:
                if not select.select([sock], [], [], timeout)[0]:
                    raise ScanError("Hết thời gian chờ bắt tay TLS") from None
            except SSL.WantWriteError:
                if not select.select([], [sock], [], timeout)[1]:
                    raise ScanError("Hết thời gian chờ bắt tay TLS") from None
        chain = conn.get_peer_cert_chain() or []
        certs = [c.to_cryptography() for c in chain]
        version, cipher = conn.get_protocol_version_name(), conn.get_cipher_name()
        try:
            conn.shutdown()
        except SSL.Error:
            pass
    except (SSL.Error, OSError) as e:
        raise ScanError(f"Bắt tay TLS thất bại: {e}") from None
    finally:
        sock.close()
    return certs, version, cipher


def probe_handshake(ip, port, sni, timeout, min_v=None, max_v=None, ciphers="DEFAULT:@SECLEVEL=0") -> bool:
    """Thử bắt tay với tham số giới hạn; True nếu máy chủ chấp nhận."""
    try:
        ctx = _client_context(min_v, max_v, ciphers)
    except (ssl.SSLError, ValueError):
        return False  # OpenSSL phía client không hỗ trợ tổ hợp này
    try:
        with socket.create_connection((ip, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=None if _is_ip(sni) else sni):
                return True
    except (ssl.SSLError, OSError):
        return False


def fetch_hsts(ip, port, sni, timeout) -> str | None:
    req = (f"HEAD / HTTP/1.1\r\nHost: {sni}\r\nUser-Agent: CertGuard\r\nConnection: close\r\n\r\n").encode()
    try:
        with socket.create_connection((ip, port), timeout=timeout) as sock:
            with _client_context().wrap_socket(sock, server_hostname=None if _is_ip(sni) else sni) as s:
                s.sendall(req)
                data = b""
                while b"\r\n\r\n" not in data and len(data) < 65536:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    data += chunk
    except (ssl.SSLError, OSError):
        return None
    for line in data.decode("latin-1").split("\r\n"):
        if line.lower().startswith("strict-transport-security:"):
            return line.split(":", 1)[1].strip()
    return ""


# ---------------------------------------------------------------------------
# 4. Phân tích chứng thư
# ---------------------------------------------------------------------------
def _is_ip(s: str) -> bool:
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False


def name_attr(name: x509.Name, oid) -> str:
    vals = name.get_attributes_for_oid(oid)
    return vals[0].value if vals else ""


def get_san(cert) -> list[str]:
    try:
        ext = cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME).value
    except x509.ExtensionNotFound:
        return []
    return ext.get_values_for_type(x509.DNSName) + [str(i) for i in ext.get_values_for_type(x509.IPAddress)]


def hostname_matches(host: str, names: list[str]) -> bool:
    host = host.lower()
    for n in names:
        n = n.lower()
        if n == host:
            return True
        # Wildcard chỉ khớp đúng 1 nhãn: *.example.com khớp a.example.com, không khớp a.b.example.com
        if n.startswith("*.") and host.count(".") >= 2:
            if host.split(".", 1)[1] == n[2:]:
                return True
    return False


def key_info(cert) -> tuple[str, int]:
    k = cert.public_key()
    if isinstance(k, rsa.RSAPublicKey):
        return "RSA", k.key_size
    if isinstance(k, ec.EllipticCurvePublicKey):
        return f"ECDSA ({k.curve.name})", k.curve.key_size
    if isinstance(k, ed25519.Ed25519PublicKey):
        return "Ed25519", 256
    if isinstance(k, ed448.Ed448PublicKey):
        return "Ed448", 456
    if isinstance(k, dsa.DSAPublicKey):
        return "DSA", k.key_size
    return type(k).__name__, 0


def is_self_signed(cert) -> bool:
    if cert.issuer != cert.subject:
        return False
    try:
        cert.verify_directly_issued_by(cert)
        return True
    except Exception:
        return False


def cert_summary(cert) -> dict:
    algo, bits = key_info(cert)
    sig = cert.signature_hash_algorithm.name.upper() if cert.signature_hash_algorithm else "N/A"
    return {
        "subject": cert.subject.rfc4514_string(),
        "issuer": cert.issuer.rfc4514_string(),
        "cn": name_attr(cert.subject, NameOID.COMMON_NAME),
        "issuer_cn": name_attr(cert.issuer, NameOID.COMMON_NAME),
        "issuer_org": name_attr(cert.issuer, NameOID.ORGANIZATION_NAME),
        "san": get_san(cert),
        "serial": format(cert.serial_number, "X"),
        "not_before": cert.not_valid_before_utc.isoformat(),
        "not_after": cert.not_valid_after_utc.isoformat(),
        "key_algo": algo,
        "key_bits": bits,
        "sig_algo": f"{sig} with {algo.split(' ')[0]}",
        "sha256": cert.fingerprint(hashes.SHA256()).hex(":").upper(),
        "is_ca": _is_ca(cert),
        "self_signed": is_self_signed(cert),
        "pem": cert.public_bytes(serialization.Encoding.PEM).decode(),
    }


def _is_ca(cert) -> bool:
    try:
        return cert.extensions.get_extension_for_class(x509.BasicConstraints).value.ca
    except x509.ExtensionNotFound:
        return False


# ---------------------------------------------------------------------------
# 5. Chuỗi tin cậy
# ---------------------------------------------------------------------------
_MOZILLA_ROOTS: list | None = None


def load_roots(extra_dir: Path | None) -> list[x509.Certificate]:
    """Kho CA tin cậy = bộ Mozilla (certifi) + các root do quản trị viên thêm (vd: Root CA nội bộ của tổ chức)."""
    global _MOZILLA_ROOTS
    if _MOZILLA_ROOTS is None:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _MOZILLA_ROOTS = x509.load_pem_x509_certificates(Path(certifi.where()).read_bytes())
    roots = list(_MOZILLA_ROOTS)
    if extra_dir and extra_dir.exists():
        for f in sorted(extra_dir.glob("*.pem")):
            try:
                roots += x509.load_pem_x509_certificates(f.read_bytes())
            except ValueError:
                pass
    return roots


def analyze_chain(host, certs, roots, now) -> tuple[list[dict], dict]:
    """
    Dựng lại đường đi leaf -> ... -> root từ những gì máy chủ gửi,
    rồi xác thực bằng bộ xác thực Web PKI của thư viện cryptography.
    """
    leaf = certs[0]
    root_by_subject = {}
    for r in roots:
        root_by_subject.setdefault(r.subject, []).append(r)

    # Dựng đường đi theo quan hệ issuer -> subject
    path, cur, pool = [leaf], leaf, list(certs[1:])
    while not is_self_signed(cur):
        nxt = next((c for c in pool if c.subject == cur.issuer), None)
        if not nxt:
            break
        path.append(nxt)
        pool.remove(nxt)
        cur = nxt

    top = path[-1]
    trusted_root = None
    if is_self_signed(top):
        trusted_root = next((r for r in root_by_subject.get(top.subject, []) if r == top), None)
    else:
        for r in root_by_subject.get(top.issuer, []):
            try:
                top.verify_directly_issued_by(r)
                trusted_root = r
                break
            except Exception:
                continue

    info = {"path_complete": bool(trusted_root), "anchor": None, "verifier_error": None,
            "trusted": False, "problem": None}
    if trusted_root:
        info["anchor"] = trusted_root.subject.rfc4514_string()
    elif is_self_signed(top) and len(path) == 1:
        info["problem"] = "self_signed"
    elif is_self_signed(top) or len(path) > 1:
        # Chuỗi lên tới một CA (root hoặc trung gian) mà kho tin cậy không biết
        info["problem"] = "untrusted_root"
        info["unknown_issuer"] = top.issuer.rfc4514_string()
    else:
        # Máy chủ chỉ gửi chứng thư lá và không tìm được CA phát hành trong kho
        info["problem"] = "incomplete_chain"

    # Xác thực đầy đủ theo chuẩn RFC 5280 / CA-Browser Forum
    try:
        verifier = (PolicyBuilder().store(Store(roots)).time(now)
                    .build_server_verifier(_subject_for(host)))
        verifier.verify(leaf, list(certs[1:]))
        info["trusted"] = True
    except VerificationError as e:
        info["verifier_error"] = str(e)
    except Exception as e:  # tên miền lạ, chứng thư quá dị dạng...
        info["verifier_error"] = f"{type(e).__name__}: {e}"

    chain_view = []
    for c in path + ([trusted_root] if trusted_root and trusted_root not in path else []):
        s = cert_summary(c)
        s["role"] = "leaf" if c is leaf else ("root" if is_self_signed(c) else "intermediate")
        s["from_store"] = c is trusted_root and c not in certs
        chain_view.append(s)
    extra = [c for c in certs[1:] if c not in path]
    for c in extra:
        s = cert_summary(c)
        s["role"] = "extra"
        s["from_store"] = False
        chain_view.append(s)
    return chain_view, info


def _subject_for(host: str):
    if _is_ip(host):
        return x509.IPAddress(ipaddress.ip_address(host))
    return x509.DNSName(host)


# ---------------------------------------------------------------------------
# 7. Thu hồi
# ---------------------------------------------------------------------------
def check_revocation(leaf, issuer, allowlist, timeout) -> dict:
    res = {"method": None, "status": "unknown", "detail": "Chứng thư không khai báo OCSP/CRL"}
    ocsp_urls, crl_urls = [], []
    try:
        aia = leaf.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_INFORMATION_ACCESS).value
        ocsp_urls = [d.access_location.value for d in aia
                     if d.access_method == x509.AuthorityInformationAccessOID.OCSP]
    except x509.ExtensionNotFound:
        pass
    try:
        cdp = leaf.extensions.get_extension_for_oid(ExtensionOID.CRL_DISTRIBUTION_POINTS).value
        crl_urls = [n.value for p in cdp for n in (p.full_name or []) if isinstance(n, x509.UniformResourceIdentifier)]
    except x509.ExtensionNotFound:
        pass

    if ocsp_urls and issuer is not None:
        url = ocsp_urls[0]
        res["method"] = "OCSP"
        try:
            check_url_safe(url, allowlist)
            req = ocsp.OCSPRequestBuilder().add_certificate(leaf, issuer, hashes.SHA1()).build()
            http = urllib.request.Request(url, data=req.public_bytes(serialization.Encoding.DER),
                                          headers={"Content-Type": "application/ocsp-request"})
            with urllib.request.urlopen(http, timeout=timeout) as r:
                resp = ocsp.load_der_ocsp_response(r.read(1_000_000))
            if resp.response_status != ocsp.OCSPResponseStatus.SUCCESSFUL:
                res.update(status="unknown", detail=f"Máy chủ OCSP trả lời: {resp.response_status.name}")
            else:
                st = resp.certificate_status
                if st == ocsp.OCSPCertStatus.REVOKED:
                    res.update(status="revoked",
                               detail=f"Bị thu hồi lúc {resp.revocation_time_utc:%Y-%m-%d %H:%M} UTC")
                elif st == ocsp.OCSPCertStatus.GOOD:
                    res.update(status="good", detail=f"OCSP xác nhận còn hiệu lực ({url})")
                else:
                    res.update(status="unknown", detail="OCSP không biết chứng thư này")
            return res
        except BlockedTarget as e:
            res.update(status="unknown", detail=f"URL OCSP bị chặn: {e}")
            return res
        except Exception as e:
            res.update(status="unknown", detail=f"Không truy vấn được OCSP: {e}")
            if not crl_urls:
                return res

    if crl_urls:
        url = crl_urls[0]
        res["method"] = "CRL"
        try:
            check_url_safe(url, allowlist)
            with urllib.request.urlopen(url, timeout=timeout) as r:
                data = r.read(20_000_000)
            try:
                crl = x509.load_der_x509_crl(data)
            except ValueError:
                crl = x509.load_pem_x509_crl(data)
            if issuer is not None and not crl.is_signature_valid(issuer.public_key()):
                res.update(status="unknown", detail="Chữ ký CRL không hợp lệ")
            elif (rev := crl.get_revoked_certificate_by_serial_number(leaf.serial_number)) is not None:
                res.update(status="revoked",
                           detail=f"Có trong CRL, thu hồi lúc {rev.revocation_date_utc:%Y-%m-%d %H:%M} UTC")
            else:
                res.update(status="good", detail=f"Không có trong CRL ({url})")
        except BlockedTarget as e:
            res.update(status="unknown", detail=f"URL CRL bị chặn: {e}")
        except Exception as e:
            res.update(status="unknown", detail=f"Không tải được CRL: {e}")
    return res


# ---------------------------------------------------------------------------
# 8. Chấm điểm
# ---------------------------------------------------------------------------
def grade_from(findings: list[Finding], has_hsts: bool) -> str:
    grade = "A+"
    for f in findings:
        if f.cap and GRADES.index(f.cap) > GRADES.index(grade):
            grade = f.cap
    if not has_hsts and grade == "A+":
        grade = "A"
    return grade


def status_from(findings: list[Finding]) -> str:
    sev = {f.severity for f in findings}
    if CRITICAL in sev:
        return "error"
    if HIGH in sev or MEDIUM in sev:
        return "warning"
    return "ok"


# ---------------------------------------------------------------------------
# Hàm chính
# ---------------------------------------------------------------------------
def scan(target: str, port: int | None = None, opts: ScanOptions | None = None) -> dict:
    opts = opts or ScanOptions()
    host, p = normalize_target(target if port is None else f"{target}:{port}")
    ip = resolve_safe(host, p, opts.allowlist)
    now = dt.datetime.now(UTC)

    certs, version, cipher = fetch_chain(ip, p, host, opts.timeout)
    if not certs:
        raise ScanError("Máy chủ không gửi chứng thư nào")
    leaf = certs[0]
    findings: list[Finding] = []
    add = lambda *a, **k: findings.append(Finding(*a, **k))

    # --- Thời hạn
    nb, na = leaf.not_valid_before_utc, leaf.not_valid_after_utc
    days_left = (na - now).total_seconds() / 86400
    if now > na:
        add("expired", CRITICAL, f"Chứng thư đã hết hạn {int(-days_left)} ngày (từ {na:%d/%m/%Y})", "F")
    elif now < nb:
        add("not_yet_valid", CRITICAL, f"Chứng thư chưa có hiệu lực (bắt đầu {nb:%d/%m/%Y})", "F")
    elif days_left <= opts.critical_days:
        add("expiring_critical", HIGH, f"Chứng thư chỉ còn {days_left:.1f} ngày là hết hạn")
    elif days_left <= opts.warn_days:
        add("expiring", MEDIUM, f"Chứng thư còn {int(days_left)} ngày là hết hạn")
    validity_days = (na - nb).days
    if validity_days > 398:
        add("long_validity", LOW,
            f"Thời hạn {validity_days} ngày vượt mức 398 ngày mà trình duyệt chấp nhận cho CA công cộng")

    # --- Hostname
    names = get_san(leaf)
    if not names:
        add("no_san", HIGH, "Chứng thư không có Subject Alternative Name (trình duyệt hiện đại yêu cầu)", "F")
    if not hostname_matches(host, names):
        add("hostname_mismatch", CRITICAL,
            f"Sai tên miền: chứng thư cấp cho {', '.join(names) or name_attr(leaf.subject, NameOID.COMMON_NAME)}, "
            f"không phải {host}", "F")

    # --- Khóa và thuật toán ký
    algo, bits = key_info(leaf)
    if algo == "RSA" and bits < 2048:
        add("weak_key", HIGH, f"Khóa RSA chỉ {bits} bit (tối thiểu 2048 bit)", "C" if bits >= 1024 else "F")
    if algo.startswith("ECDSA") and bits < 256:
        add("weak_key", HIGH, f"Khóa ECDSA chỉ {bits} bit", "C")
    h = leaf.signature_hash_algorithm
    if h is not None and h.name in ("md5", "sha1"):
        add("weak_signature", CRITICAL, f"Chứng thư ký bằng {h.name.upper()} đã bị phá vỡ", "F")

    # --- Chuỗi tin cậy
    roots = load_roots(opts.extra_roots_dir)
    chain_view, chain_info = analyze_chain(host, certs, roots, now)
    problem = chain_info["problem"]
    if problem == "self_signed":
        add("self_signed", CRITICAL, "Chứng thư tự ký, không do CA tin cậy nào cấp", "F")
    elif problem == "untrusted_root":
        add("untrusted_root", CRITICAL,
            f"Chuỗi kết thúc ở CA không nằm trong kho tin cậy ({chain_info.get('unknown_issuer', '')})", "F")
    elif problem == "incomplete_chain":
        add("incomplete_chain", HIGH,
            "Máy chủ không gửi chứng thư trung gian (chuỗi không đầy đủ). "
            "Một số trình duyệt/ứng dụng sẽ báo lỗi", "B")
    elif not chain_info["trusted"] and not any(f.severity == CRITICAL for f in findings):
        add("chain_invalid", HIGH, f"Bộ xác thực X.509 từ chối chuỗi: {chain_info['verifier_error']}", "C")

    # --- Thu hồi
    issuer_cert = None
    for c in certs[1:] + roots:
        if c.subject == leaf.issuer:
            try:
                leaf.verify_directly_issued_by(c)
                issuer_cert = c
                break
            except Exception:
                continue
    revocation = (check_revocation(leaf, issuer_cert, opts.allowlist, opts.timeout)
                  if opts.check_revocation else {"method": None, "status": "skipped", "detail": "Bỏ qua"})
    if revocation["status"] == "revoked":
        add("revoked", CRITICAL, f"Chứng thư đã bị CA thu hồi. {revocation['detail']}", "F")

    # --- Cấu hình TLS
    protocols = {}
    for label, v in [("TLS 1.0", ssl.TLSVersion.TLSv1), ("TLS 1.1", ssl.TLSVersion.TLSv1_1),
                     ("TLS 1.2", ssl.TLSVersion.TLSv1_2), ("TLS 1.3", ssl.TLSVersion.TLSv1_3)]:
        protocols[label] = probe_handshake(ip, p, host, opts.timeout, v, v)
    old = [k for k in ("TLS 1.0", "TLS 1.1") if protocols[k]]
    if old:
        add("old_tls", MEDIUM, f"Máy chủ còn hỗ trợ {', '.join(old)} (đã bị loại bỏ theo RFC 8996)", "B")
    if not protocols["TLS 1.2"] and not protocols["TLS 1.3"]:
        add("no_modern_tls", HIGH, "Không hỗ trợ TLS 1.2/1.3", "F")
    if not protocols["TLS 1.3"]:
        add("no_tls13", LOW, "Chưa bật TLS 1.3")

    weak_cipher = probe_handshake(ip, p, host, opts.timeout, None, ssl.TLSVersion.TLSv1_2,
                                  "RC4:3DES:DES:NULL:EXPORT:aNULL:@SECLEVEL=0")
    if weak_cipher:
        add("weak_cipher", HIGH, "Máy chủ chấp nhận cipher yếu (3DES/RC4/NULL...)", "C")
    no_pfs = probe_handshake(ip, p, host, opts.timeout, None, ssl.TLSVersion.TLSv1_2, "kRSA:@SECLEVEL=0")
    if no_pfs:
        add("no_pfs", MEDIUM, "Chấp nhận trao đổi khóa RSA tĩnh (không có Forward Secrecy)", "B")

    hsts = fetch_hsts(ip, p, host, opts.timeout)
    has_hsts = bool(hsts)
    if not has_hsts:
        add("no_hsts", LOW, "Không có header Strict-Transport-Security (HSTS)")

    grade = grade_from(findings, has_hsts)
    status = status_from(findings)
    order = [CRITICAL, HIGH, MEDIUM, LOW, INFO]
    findings.sort(key=lambda f: order.index(f.severity))

    return {
        "host": host,
        "port": p,
        "ip": ip,
        "scanned_at": now.isoformat(),
        "status": status,
        "grade": grade,
        "days_left": round(days_left, 2),
        "leaf": cert_summary(leaf),
        "chain": chain_view,
        "chain_info": chain_info,
        "certs_sent": len(certs),
        "negotiated": {"version": version, "cipher": cipher},
        "protocols": protocols,
        "weak_cipher": weak_cipher,
        "no_pfs": no_pfs,
        "hsts": hsts,
        "revocation": revocation,
        "findings": [f.__dict__ for f in findings],
        "verify_cmd": (f"echo Q | openssl s_client -connect {host}:{p} -servername {host} "
                       f"-verify_hostname {host} -showcerts"),
    }


def analyze_pem(data: bytes, roots_dir: Path | None = None) -> dict:
    """Phân tích file chứng thư người dùng tải lên (không kết nối mạng)."""
    try:
        certs = x509.load_pem_x509_certificates(data)
    except ValueError:
        try:
            certs = [x509.load_der_x509_certificate(data)]
        except ValueError:
            raise ScanError("File không phải chứng thư PEM/DER hợp lệ") from None
    now = dt.datetime.now(UTC)
    out = []
    for c in certs:
        s = cert_summary(c)
        s["days_left"] = round((c.not_valid_after_utc - now).total_seconds() / 86400, 1)
        s["expired"] = now > c.not_valid_after_utc
        out.append(s)
    return {"certs": out}


if __name__ == "__main__":  # Chạy thử nhanh từ dòng lệnh: python scanner.py good.certguard.webservers:8443
    import json
    import sys
    o = ScanOptions(allowlist=["*.certguard.webservers"], extra_roots_dir=Path(__file__).parent / "trusted_roots")
    r = scan(sys.argv[1], opts=o)
    for c in r["chain"]:
        c.pop("pem", None)
    r["leaf"].pop("pem", None)
    print(json.dumps(r, indent=2, ensure_ascii=False))
