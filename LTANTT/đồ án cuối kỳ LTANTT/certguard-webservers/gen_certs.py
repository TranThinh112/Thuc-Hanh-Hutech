"""
Sinh chứng thư THẬT cho các web server demo của CertGuard (Root CA -> Intermediate CA -> chứng thư máy chủ).

Mọi chứng thư đều được ký bằng khóa RSA thật, có thể kiểm chứng độc lập bằng
openssl hoặc trình duyệt. Không có dữ liệu "giả" nào được ghi vào CSDL.

Chạy:  pip install cryptography
       python gen_certs.py
       python gen_certs.py --expiring-days 5 --weak-bits 1024
"""
import argparse
import datetime
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

BASE = Path(__file__).resolve().parent
CERTS = BASE / "certs"
HTML = BASE / "html"
DOMAIN = "certguard.webservers"
UTC = datetime.timezone.utc
NOW = datetime.datetime.now(UTC)
DAY = datetime.timedelta(days=1)


def new_key(bits: int = 2048):
    return rsa.generate_private_key(public_exponent=65537, key_size=bits)


def make_name(cn: str) -> x509.Name:
    return x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "VN"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CertGuard Internal"),
        x509.NameAttribute(NameOID.COMMON_NAME, cn),
    ])


def save_key(key, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption(),
    ))


def save_certs(certs, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(c.public_bytes(serialization.Encoding.PEM) for c in certs))


def make_ca(cn, key, issuer_cert=None, issuer_key=None, path_len=None, days=3650):
    subject = make_name(cn)
    issuer = issuer_cert.subject if issuer_cert else subject
    signer = issuer_key or key
    signer_pub = (issuer_key or key).public_key()
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(NOW - DAY)
        .not_valid_after(NOW + days * DAY)
        .add_extension(x509.BasicConstraints(ca=True, path_length=path_len), critical=True)
        .add_extension(x509.KeyUsage(
            digital_signature=True, content_commitment=False, key_encipherment=False,
            data_encipherment=False, key_agreement=False, key_cert_sign=True,
            crl_sign=True, encipher_only=False, decipher_only=False), critical=True)
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
        .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(signer_pub), critical=False)
    )
    return builder.sign(signer, hashes.SHA256())


def make_leaf(san_host, key, not_before, not_after, issuer_cert=None, issuer_key=None):
    """issuer_cert=None nghĩa là chứng thư tự ký (self-signed)."""
    subject = make_name(san_host)
    issuer = issuer_cert.subject if issuer_cert else subject
    signer = issuer_key or key
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(not_before)
        .not_valid_after(not_after)
        .add_extension(x509.SubjectAlternativeName([x509.DNSName(san_host)]), critical=False)
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(x509.KeyUsage(
            digital_signature=True, content_commitment=False, key_encipherment=True,
            data_encipherment=False, key_agreement=False, key_cert_sign=False,
            crl_sign=False, encipher_only=False, decipher_only=False), critical=True)
        .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
        .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(signer.public_key()), critical=False)
    )
    return builder.sign(signer, hashes.SHA256())


def write_page(name: str, title: str, desc: str) -> None:
    folder = HTML / name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(
        f"<!doctype html><html lang='vi'><meta charset='utf-8'><title>{title}</title>"
        f"<body style='font-family:sans-serif;max-width:640px;margin:40px auto'>"
        f"<h1>{title}</h1><p>{desc}</p><p>Máy chủ: <b>{name}.{DOMAIN}</b></p></body></html>",
        encoding="utf-8",
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expiring-days", type=int, default=5,
                    help="Số ngày còn lại của chứng thư 'sắp hết hạn' (mặc định 5)")
    ap.add_argument("--weak-bits", type=int, default=1024,
                    help="Độ dài khóa RSA cho máy chủ 'yếu' (mặc định 1024)")
    args = ap.parse_args()

    # 1) Chuỗi tin cậy: Root CA -> Intermediate CA
    root_key = new_key(4096)
    root = make_ca("CertGuard Internal Root CA", root_key, path_len=1, days=3650)
    inter_key = new_key(2048)
    inter = make_ca("CertGuard Internal Issuing CA", inter_key,
                    issuer_cert=root, issuer_key=root_key, path_len=0, days=1825)
    save_certs([root], CERTS / "ca" / "root.pem")
    save_key(root_key, CERTS / "ca" / "root.key")
    save_certs([inter], CERTS / "ca" / "intermediate.pem")
    save_key(inter_key, CERTS / "ca" / "intermediate.key")

    # 2) Các web server: (tên, mô tả, hàm tạo -> (key, [chuỗi gửi đi]))
    def signed(host, nb, na, bits=2048, send_chain=True):
        k = new_key(bits)
        c = make_leaf(host, k, nb, na, issuer_cert=inter, issuer_key=inter_key)
        return k, ([c, inter] if send_chain else [c])

    def self_signed(host):
        k = new_key(2048)
        return k, [make_leaf(host, k, NOW - DAY, NOW + 365 * DAY)]

    h = lambda n: f"{n}.{DOMAIN}"
    servers = {
        "good":       ("Chứng thư hợp lệ, cấu hình chuẩn",
                       lambda: signed(h("good"), NOW - DAY, NOW + 365 * DAY)),
        "expiring":   (f"Chứng thư còn {args.expiring_days} ngày là hết hạn",
                       lambda: signed(h("expiring"), NOW - 85 * DAY, NOW + args.expiring_days * DAY)),
        "expired":    ("Chứng thư đã hết hạn",
                       lambda: signed(h("expired"), NOW - 400 * DAY, NOW - 10 * DAY)),
        "selfsigned": ("Chứng thư tự ký, không do CA nào cấp",
                       lambda: self_signed(h("selfsigned"))),
        "wronghost":  ("Chứng thư cấp cho tên miền khác (sai hostname)",
                       lambda: signed(f"khac.{DOMAIN}", NOW - DAY, NOW + 365 * DAY)),
        "incomplete": ("Máy chủ không gửi chứng thư trung gian (thiếu chuỗi)",
                       lambda: signed(h("incomplete"), NOW - DAY, NOW + 365 * DAY, send_chain=False)),
        "weak":       (f"Khóa RSA {args.weak_bits} bit, bật TLS 1.0/1.1, cipher yếu, không HSTS",
                       lambda: signed(h("weak"), NOW - DAY, NOW + 365 * DAY, bits=args.weak_bits)),
    }

    for name, (desc, build) in servers.items():
        key, chain = build()
        save_key(key, CERTS / name / "privkey.pem")
        save_certs(chain, CERTS / name / "fullchain.pem")
        write_page(name, f"Web server: {name}", desc)
        leaf = chain[0]
        print(f"[+] {name:<11} hết hạn {leaf.not_valid_after_utc:%Y-%m-%d %H:%M} UTC  | {desc}")

    print(f"\nĐã sinh chứng thư vào: {CERTS}")
    print("Root CA để đối chứng: certs/ca/root.pem")


if __name__ == "__main__":
    main()
