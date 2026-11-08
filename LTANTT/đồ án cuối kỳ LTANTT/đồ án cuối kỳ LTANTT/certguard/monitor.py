"""
Giám sát: quét một/nhiều domain, lưu kết quả, phát hiện thay đổi và gửi cảnh báo.
Được gọi từ giao diện web (quét thủ công) và từ bộ lập lịch (quét định kỳ).
"""
import datetime as dt
import html
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import db
import notifier
import scanner

log = logging.getLogger("certguard.monitor")
ROOTS_DIR = Path(__file__).resolve().parent / "trusted_roots"

# Các lỗi đáng gửi cảnh báo ngay (lỗi cấu hình nhẹ như thiếu HSTS thì chỉ hiển thị)
ALERT_CODES = {"expired", "not_yet_valid", "expiring", "expiring_critical", "self_signed",
               "untrusted_root", "hostname_mismatch", "revoked", "incomplete_chain", "weak_signature"}


def options_from(settings: dict) -> scanner.ScanOptions:
    return scanner.ScanOptions(
        allowlist=[x for x in settings.get("allowlist", "").replace(",", "\n").splitlines() if x.strip()],
        extra_roots_dir=ROOTS_DIR,
        warn_days=int(settings.get("warn_days", 30)),
        critical_days=int(settings.get("critical_days", 7)),
    )


def scan_domain(conn, domain, triggered_by: str) -> dict:
    """Quét 1 domain đã đăng ký. Trả về {'scan_id', 'result' | 'error', 'alerts'}."""
    settings = db.get_settings(conn)
    prev = conn.execute("SELECT fingerprint FROM scans WHERE domain_id = ? AND fingerprint IS NOT NULL "
                        "ORDER BY id DESC LIMIT 1", (domain["id"],)).fetchone()
    try:
        result = scanner.scan(domain["host"], domain["port"], options_from(settings))
    except scanner.ScanError as e:
        scan_id = db.save_scan(conn, domain["id"], domain["host"], domain["port"], triggered_by, error=str(e))
        alerts = _alert(conn, domain, scan_id, "unreachable", [str(e)], triggered_by, settings)
        return {"scan_id": scan_id, "error": str(e), "alerts": alerts}

    # Phát hiện chứng thư bị thay đổi so với lần quét trước
    if prev and prev["fingerprint"] != result["leaf"]["sha256"]:
        result["findings"].insert(0, {
            "code": "cert_changed", "severity": "info", "cap": None,
            "message": f"Chứng thư đã THAY ĐỔI so với lần quét trước (fingerprint cũ {prev['fingerprint'][:23]}...)"})

    scan_id = db.save_scan(conn, domain["id"], domain["host"], domain["port"], triggered_by, result=result)
    problems = [f["message"] for f in result["findings"] if f["code"] in ALERT_CODES | {"cert_changed"}]
    alerts = _alert(conn, domain, scan_id, result["status"], problems, triggered_by, settings, result) if problems else []
    return {"scan_id": scan_id, "result": result, "alerts": alerts}


def _alert(conn, domain, scan_id, level, problems, triggered_by, settings, result=None):
    message = " | ".join(problems)
    # Quét định kỳ: không gửi lặp lại cùng một nội dung trong thời gian chờ (cooldown)
    if triggered_by == "schedule":
        cooldown = int(settings.get("alert_cooldown_minutes", 60))
        since = (dt.datetime.utcnow() - dt.timedelta(minutes=cooldown)).strftime("%Y-%m-%d %H:%M:%S")
        dup = conn.execute("SELECT 1 FROM alerts WHERE domain_id = ? AND message = ? AND success = 1 "
                           "AND sent_at >= ?", (domain["id"], message, since)).fetchone()
        if dup:
            return []

    icon = {"error": "🔴", "unreachable": "⚫", "warning": "🟠"}.get(level, "🔵")
    target = f"{domain['host']}:{domain['port']}"
    lines = [f"{icon} <b>CertGuard cảnh báo</b>", f"Máy chủ: <code>{html.escape(target)}</code>"]
    if domain["label"]:
        lines.append(f"Tên: {html.escape(domain['label'])}")
    if result:
        lines.append(f"Điểm: <b>{result['grade']}</b> | Còn {result['days_left']:.1f} ngày")
    lines += [f"• {html.escape(p)}" for p in problems]
    lines.append(f"Thời gian: {dt.datetime.now(dt.timezone(dt.timedelta(hours=7))):%d/%m/%Y %H:%M}")
    sent = notifier.notify("\n".join(lines), f"[CertGuard] {target}: {problems[0][:80]}")

    out = []
    for channel, ok, detail in sent or [("none", False, "Chưa cấu hình kênh cảnh báo nào")]:
        conn.execute("INSERT INTO alerts(domain_id, scan_id, level, message, channel, success, detail) "
                     "VALUES (?,?,?,?,?,?,?)", (domain["id"], scan_id, level, message, channel, int(ok), detail))
        out.append({"channel": channel, "ok": ok, "detail": detail})
    conn.commit()
    return out


def scan_all(triggered_by: str = "schedule") -> int:
    """Quét song song mọi domain đang bật. Mỗi luồng dùng kết nối CSDL riêng."""
    conn = db.connect()
    domains = conn.execute("SELECT * FROM domains WHERE enabled = 1").fetchall()
    conn.close()

    def work(d):
        c = db.connect()
        try:
            scan_domain(c, d, triggered_by)
        except Exception:
            log.exception("Lỗi khi quét %s", d["host"])
        finally:
            c.close()

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(work, domains))
    log.info("Đã quét %d domain (%s)", len(domains), triggered_by)
    return len(domains)
