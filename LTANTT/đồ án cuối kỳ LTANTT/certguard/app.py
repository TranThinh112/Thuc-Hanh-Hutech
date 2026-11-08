"""
CertGuard - Hệ thống quản lý và kiểm tra chứng thư số SSL/TLS cho máy chủ Web.

Chạy:  python app.py      rồi mở http://127.0.0.1:5000
"""
import datetime as dt
import json
import logging
import os
import secrets
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from flask import (Flask, abort, flash, g, redirect, render_template, request,
                   session, url_for)

import db
import monitor
import notifier
import scanner
import security
from security import admin_required, audit, login_required

BASE = Path(__file__).resolve().parent
VN_TZ = dt.timezone(dt.timedelta(hours=7))
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def load_env(path: Path) -> None:
    """Đọc file .env đơn giản (KEY=VALUE) vào biến môi trường."""
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def secret_key() -> str:
    """SECRET_KEY ngẫu nhiên, sinh 1 lần và lưu trong instance/ (không đưa vào mã nguồn)."""
    if os.environ.get("SECRET_KEY"):
        return os.environ["SECRET_KEY"]
    f = BASE / "instance" / "secret_key"
    f.parent.mkdir(exist_ok=True)
    if not f.exists():
        f.write_text(secrets.token_hex(32))
        try:
            os.chmod(f, 0o600)
        except OSError:
            pass
    return f.read_text().strip()


load_env(BASE / ".env")
app = Flask(__name__)
app.config.update(
    SECRET_KEY=secret_key(),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=dt.timedelta(hours=8),
    MAX_CONTENT_LENGTH=1 * 1024 * 1024,  # giới hạn upload 1MB
)
app.teardown_appcontext(db.close_db)
app.after_request(security.security_headers)
app.jinja_env.globals["csrf_token"] = security.csrf_token


# ---------------------------------------------------------------- bộ lọc hiển thị
@app.template_filter("vntime")
def vntime(value, fmt="%d/%m/%Y %H:%M"):
    if not value:
        return "—"
    t = dt.datetime.fromisoformat(str(value).replace(" ", "T"))
    if t.tzinfo is None:
        t = t.replace(tzinfo=dt.timezone.utc)
    return t.astimezone(VN_TZ).strftime(fmt)


@app.template_filter("days")
def days_filter(v):
    if v is None:
        return "—"
    return f"{v:.0f} ngày" if abs(v) >= 1 else f"{v * 24:.0f} giờ"


STATUS_VI = {"ok": "Hợp lệ", "warning": "Cảnh báo", "error": "Lỗi", "unreachable": "Mất kết nối", None: "Chưa quét"}
SEV_VI = {"critical": "Nghiêm trọng", "high": "Cao", "medium": "Trung bình", "low": "Thấp", "info": "Thông tin"}
app.jinja_env.globals.update(STATUS_VI=STATUS_VI, SEV_VI=SEV_VI)


# ---------------------------------------------------------------- vòng đời request
@app.before_request
def before():
    security.check_csrf()
    g.user = None
    uid = session.get("uid")
    if uid:
        row = db.get_db().execute("SELECT id, username, role FROM users WHERE id = ?", (uid,)).fetchone()
        g.user = dict(row) if row else None
        if not row:
            session.clear()


@app.errorhandler(400)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(413)
def http_error(e):
    msg = {413: "File quá lớn (tối đa 1MB)"}.get(e.code, e.description)
    return render_template("error.html", code=e.code, message=msg), e.code


# ---------------------------------------------------------------- đăng nhập
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = db.get_db()
        username = request.form.get("username", "").strip()
        user, err = security.authenticate(conn, username, request.form.get("password", ""))
        if user:
            session.clear()  # chống session fixation
            session["uid"] = user["id"]
            session.permanent = True
            g.user = user
            audit(conn, "login_success", "Đăng nhập thành công")
            nxt = request.args.get("next", "")
            return redirect(nxt if nxt.startswith("/") and not nxt.startswith("//") else url_for("dashboard"))
        audit(conn, "login_failed", err, username=username or "(trống)")
        flash(err, "error")
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    if g.user:
        audit(db.get_db(), "logout", "")
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------- dashboard
@app.route("/")
@login_required
def dashboard():
    conn = db.get_db()
    rows = db.latest_scans(conn)
    stats = {"total": len(rows), "ok": 0, "warning": 0, "error": 0, "unreachable": 0, "never": 0}
    for r in rows:
        stats[r["status"] or "never"] += 1
    expiring = [r for r in rows if r["days_left"] is not None and r["days_left"] <= 30]
    alerts = conn.execute("SELECT a.*, d.host, d.port FROM alerts a JOIN domains d ON d.id = a.domain_id "
                          "ORDER BY a.id DESC LIMIT 6").fetchall()
    total_scans = conn.execute("SELECT COUNT(*) FROM scans").fetchone()[0]
    return render_template("dashboard.html", rows=rows, stats=stats, expiring=expiring,
                           alerts=alerts, total_scans=total_scans)


# ---------------------------------------------------------------- quét nhanh
@app.route("/scan", methods=["GET", "POST"])
@login_required
def quick_scan():
    result, error, target = None, None, request.values.get("target", "")
    if request.method == "POST":
        conn = db.get_db()
        try:
            host, port = scanner.normalize_target(target)
            result = scanner.scan(host, port, monitor.options_from(db.get_settings(conn)))
            db.save_scan(conn, None, host, port, "quick", result=result)
            audit(conn, "quick_scan", f"{host}:{port} -> {result['grade']}")
        except scanner.BlockedTarget as e:
            error = str(e)
            audit(conn, "ssrf_blocked", f"{target}: {e}")
        except scanner.ScanError as e:
            error = str(e)
    exists = None
    if result:
        exists = db.get_db().execute("SELECT id FROM domains WHERE host = ? AND port = ?",
                                     (result["host"], result["port"])).fetchone()
    return render_template("scan.html", result=result, error=error, target=target, exists=exists)


# ---------------------------------------------------------------- quản lý domain
@app.route("/domains/add", methods=["POST"])
@login_required
def domain_add():
    conn = db.get_db()
    try:
        host, port = scanner.normalize_target(request.form.get("target", ""))
    except scanner.ScanError as e:
        flash(str(e), "error")
        return redirect(request.referrer or url_for("dashboard"))
    label = request.form.get("label", "").strip()[:100]
    try:
        cur = conn.execute("INSERT INTO domains(host, port, label, created_by) VALUES (?,?,?,?)",
                           (host, port, label or None, g.user["username"]))
        conn.commit()
    except db.sqlite3.IntegrityError:
        flash(f"{host}:{port} đã có trong danh sách giám sát", "error")
        return redirect(url_for("dashboard"))
    audit(conn, "domain_add", f"{host}:{port}")
    domain = conn.execute("SELECT * FROM domains WHERE id = ?", (cur.lastrowid,)).fetchone()
    out = monitor.scan_domain(conn, domain, "manual")
    flash(f"Đã thêm {host}:{port}" + (f" — không quét được: {out['error']}" if "error" in out else ""),
          "error" if "error" in out else "ok")
    return redirect(url_for("domain_detail", domain_id=domain["id"]))


def _domain_or_404(domain_id):
    d = db.get_db().execute("SELECT * FROM domains WHERE id = ?", (domain_id,)).fetchone()
    if not d:
        abort(404, "Không tìm thấy domain")
    return d


@app.route("/domains/<int:domain_id>")
@login_required
def domain_detail(domain_id):
    conn = db.get_db()
    d = _domain_or_404(domain_id)
    scan_id = request.args.get("scan", type=int)
    q = "SELECT * FROM scans WHERE domain_id = ? " + ("AND id = ? " if scan_id else "") + "ORDER BY id DESC LIMIT 1"
    current = conn.execute(q, (domain_id, scan_id) if scan_id else (domain_id,)).fetchone()
    history = conn.execute("SELECT id, scanned_at, status, grade, days_left, fingerprint, error, triggered_by "
                           "FROM scans WHERE domain_id = ? ORDER BY id DESC LIMIT 50", (domain_id,)).fetchall()
    alerts = conn.execute("SELECT * FROM alerts WHERE domain_id = ? ORDER BY id DESC LIMIT 20",
                          (domain_id,)).fetchall()
    return render_template("domain.html", d=d, current=current, result=db.load_result(current),
                           history=history, alerts=alerts)


@app.route("/domains/<int:domain_id>/scan", methods=["POST"])
@login_required
def domain_scan(domain_id):
    conn = db.get_db()
    d = _domain_or_404(domain_id)
    out = monitor.scan_domain(conn, d, "manual")
    audit(conn, "domain_scan", f"{d['host']}:{d['port']}")
    msg = f"Đã quét {d['host']}:{d['port']}"
    for a in out["alerts"]:
        msg += f" · cảnh báo {a['channel']}: {'đã gửi' if a['ok'] else a['detail']}"
    flash(msg, "error" if "error" in out else "ok")
    return redirect(url_for("domain_detail", domain_id=domain_id))


@app.route("/domains/<int:domain_id>/toggle", methods=["POST"])
@login_required
def domain_toggle(domain_id):
    conn = db.get_db()
    d = _domain_or_404(domain_id)
    conn.execute("UPDATE domains SET enabled = 1 - enabled WHERE id = ?", (domain_id,))
    conn.commit()
    audit(conn, "domain_toggle", f"{d['host']}:{d['port']} -> {'tắt' if d['enabled'] else 'bật'} giám sát")
    return redirect(url_for("domain_detail", domain_id=domain_id))


@app.route("/domains/<int:domain_id>/delete", methods=["POST"])
@admin_required
def domain_delete(domain_id):
    conn = db.get_db()
    d = _domain_or_404(domain_id)
    conn.execute("DELETE FROM domains WHERE id = ?", (domain_id,))
    conn.commit()
    audit(conn, "domain_delete", f"{d['host']}:{d['port']}")
    flash(f"Đã xóa {d['host']}:{d['port']}", "ok")
    return redirect(url_for("dashboard"))


@app.route("/scan-all", methods=["POST"])
@login_required
def scan_all():
    n = monitor.scan_all("manual")
    audit(db.get_db(), "scan_all", f"{n} domain")
    flash(f"Đã quét lại {n} domain", "ok")
    return redirect(url_for("dashboard"))


# ---------------------------------------------------------------- phân tích file chứng thư
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    result, error = None, None
    if request.method == "POST":
        f = request.files.get("certfile")
        data = f.read() if f else request.form.get("pem", "").encode()
        if not data.strip():
            error = "Chưa chọn file hoặc dán nội dung chứng thư"
        else:
            try:
                result = scanner.analyze_pem(data)
                audit(db.get_db(), "pem_analyze", f"{len(result['certs'])} chứng thư")
            except scanner.ScanError as e:
                error = str(e)
    return render_template("upload.html", result=result, error=error)


# ---------------------------------------------------------------- cài đặt (admin)
@app.route("/settings", methods=["GET", "POST"])
@admin_required
def settings():
    conn = db.get_db()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "save":
            try:
                vals = {k: int(request.form[k]) for k in
                        ("warn_days", "critical_days", "scan_interval_minutes", "alert_cooldown_minutes")}
            except (KeyError, ValueError):
                flash("Giá trị phải là số nguyên", "error")
                return redirect(url_for("settings"))
            if not (1 <= vals["critical_days"] <= vals["warn_days"] <= 365) or vals["scan_interval_minutes"] < 1:
                flash("Giá trị không hợp lệ (1 ≤ ngưỡng nghiêm trọng ≤ ngưỡng cảnh báo ≤ 365)", "error")
                return redirect(url_for("settings"))
            for k, v in vals.items():
                db.set_setting(conn, k, v)
            allow = "\n".join(x.strip().lower() for x in request.form.get("allowlist", "").splitlines() if x.strip())
            db.set_setting(conn, "allowlist", allow)
            reschedule(vals["scan_interval_minutes"])
            audit(conn, "settings_update", json.dumps({**vals, "allowlist": allow}, ensure_ascii=False))
            flash("Đã lưu cài đặt", "ok")
        elif action == "test_alert":
            res = notifier.notify("🔔 <b>CertGuard</b>: tin nhắn thử nghiệm kênh cảnh báo", "[CertGuard] Thử nghiệm")
            if not res:
                flash("Chưa cấu hình kênh cảnh báo nào trong file .env", "error")
            for ch, ok, detail in res:
                flash(f"{ch}: {detail}", "ok" if ok else "error")
        elif action == "add_root":
            f = request.files.get("rootfile")
            try:
                certs = x509.load_pem_x509_certificates(f.read() if f else b"")
                for c in certs:
                    bc = c.extensions.get_extension_for_class(x509.BasicConstraints).value
                    if not bc.ca:
                        raise ValueError("không phải chứng thư CA")
                name = "".join(ch for ch in (f.filename or "root") if ch.isalnum() or ch in "-_.")[:60]
                name = name if name.endswith(".pem") else name.rsplit(".", 1)[0] + ".pem"
                (monitor.ROOTS_DIR / name).write_bytes(b"".join(
                    c.public_bytes(serialization.Encoding.PEM) for c in certs))
                audit(conn, "trusted_root_add", f"{name}: {certs[0].subject.rfc4514_string()}")
                flash(f"Đã thêm Root CA tin cậy: {certs[0].subject.rfc4514_string()}", "ok")
            except Exception as e:
                flash(f"File Root CA không hợp lệ: {e}", "error")
        elif action == "del_root":
            name = request.form.get("name", "")
            p = (monitor.ROOTS_DIR / name).resolve()
            if p.parent == monitor.ROOTS_DIR.resolve() and p.exists():  # chống path traversal
                p.unlink()
                audit(conn, "trusted_root_delete", name)
                flash(f"Đã xóa {name}", "ok")
        return redirect(url_for("settings"))

    roots = []
    for f in sorted(monitor.ROOTS_DIR.glob("*.pem")):
        try:
            c = x509.load_pem_x509_certificates(f.read_bytes())[0]
            roots.append({"name": f.name, "subject": c.subject.rfc4514_string(),
                          "not_after": c.not_valid_after_utc.isoformat()})
        except ValueError:
            roots.append({"name": f.name, "subject": "(không đọc được)", "not_after": None})
    return render_template("settings.html", s=db.get_settings(conn), roots=roots,
                           tg=notifier.telegram_configured(), mail=notifier.email_configured())


# ---------------------------------------------------------------- người dùng (admin)
@app.route("/users", methods=["GET", "POST"])
@admin_required
def users():
    conn = db.get_db()
    if request.method == "POST":
        action, uid = request.form.get("action"), request.form.get("uid", type=int)
        if action == "create":
            username = request.form.get("username", "").strip()
            pw = request.form.get("password", "")
            role = "admin" if request.form.get("role") == "admin" else "user"
            err = security.password_policy(pw)
            if not username.isidentifier() or len(username) > 32:
                err = "Tên đăng nhập chỉ gồm chữ, số, dấu _ (tối đa 32 ký tự)"
            if err:
                flash(err, "error")
            else:
                try:
                    conn.execute("INSERT INTO users(username, password_hash, role) VALUES (?,?,?)",
                                 (username, security.hash_password(pw), role))
                    conn.commit()
                    audit(conn, "user_create", f"{username} ({role})")
                    flash(f"Đã tạo tài khoản {username}", "ok")
                except db.sqlite3.IntegrityError:
                    flash("Tên đăng nhập đã tồn tại", "error")
        elif action == "unlock" and uid:
            conn.execute("UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE id = ?", (uid,))
            conn.commit()
            audit(conn, "user_unlock", f"id={uid}")
            flash("Đã mở khóa tài khoản", "ok")
        elif action == "delete" and uid:
            if uid == g.user["id"]:
                flash("Không thể tự xóa tài khoản đang đăng nhập", "error")
            else:
                u = conn.execute("SELECT username FROM users WHERE id = ?", (uid,)).fetchone()
                conn.execute("DELETE FROM users WHERE id = ?", (uid,))
                conn.commit()
                audit(conn, "user_delete", u["username"] if u else str(uid))
                flash("Đã xóa tài khoản", "ok")
        return redirect(url_for("users"))
    rows = conn.execute("SELECT id, username, role, failed_attempts, locked_until, created_at "
                        "FROM users ORDER BY id").fetchall()
    now = dt.datetime.utcnow().isoformat()
    return render_template("users.html", rows=rows, now=now)


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        conn = db.get_db()
        row = conn.execute("SELECT password_hash FROM users WHERE id = ?", (g.user["id"],)).fetchone()
        new = request.form.get("new", "")
        if not security.check_password_hash(row["password_hash"], request.form.get("old", "")):
            flash("Mật khẩu hiện tại không đúng", "error")
        elif new != request.form.get("confirm", ""):
            flash("Xác nhận mật khẩu không khớp", "error")
        elif err := security.password_policy(new):
            flash(err, "error")
        else:
            conn.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                         (security.hash_password(new), g.user["id"]))
            conn.commit()
            audit(conn, "password_change", "")
            flash("Đã đổi mật khẩu", "ok")
        return redirect(url_for("account"))
    return render_template("account.html")


@app.route("/audit")
@admin_required
def audit_log():
    rows = db.get_db().execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT 300").fetchall()
    return render_template("audit.html", rows=rows)


# ---------------------------------------------------------------- lập lịch quét định kỳ
scheduler = BackgroundScheduler(timezone="UTC")


def reschedule(minutes: int):
    scheduler.add_job(monitor.scan_all, "interval", minutes=minutes, id="scan_all",
                      replace_existing=True, kwargs={"triggered_by": "schedule"},
                      next_run_time=dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=minutes))
    logging.getLogger("certguard").info("Quét định kỳ mỗi %d phút", minutes)


def start_scheduler():
    conn = db.connect()
    minutes = int(db.get_settings(conn).get("scan_interval_minutes", 1440))
    conn.close()
    scheduler.start()
    reschedule(minutes)


db.init_db()

if __name__ == "__main__":
    conn = db.connect()
    if not conn.execute("SELECT 1 FROM users LIMIT 1").fetchone():
        print("\n  Chưa có tài khoản nào. Hãy chạy:  python manage.py create-admin\n")
    conn.close()
    start_scheduler()
    host = os.environ.get("CERTGUARD_HOST", "127.0.0.1")  # mặc định chỉ nghe trên máy local
    app.run(host=host, port=int(os.environ.get("CERTGUARD_PORT", 5000)), debug=False)
