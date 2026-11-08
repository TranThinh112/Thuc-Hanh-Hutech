"""
Các cơ chế bảo mật cho chính ứng dụng CertGuard:
  - Băm mật khẩu (scrypt, có salt) qua werkzeug
  - Khóa tài khoản tạm thời khi đăng nhập sai nhiều lần (chống brute-force)
  - CSRF token cho mọi form POST
  - Phân quyền admin / user
  - Ghi nhật ký kiểm toán (audit log)
  - Header bảo mật HTTP (CSP, X-Frame-Options, ...)
"""
import datetime as dt
import hmac
import secrets
from functools import wraps

from flask import abort, flash, g, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

MAX_FAILED = 5
LOCK_MINUTES = 5
# Hash giả dùng khi username không tồn tại, để thời gian phản hồi giống nhau
# (tránh kẻ tấn công dò ra username nào tồn tại dựa vào thời gian)
_DUMMY_HASH = generate_password_hash("dummy-password-for-timing")


def hash_password(pw: str) -> str:
    return generate_password_hash(pw)  # mặc định: scrypt + salt ngẫu nhiên


def password_policy(pw: str) -> str | None:
    if len(pw) < 8:
        return "Mật khẩu phải có ít nhất 8 ký tự"
    if pw.isdigit() or pw.isalpha():
        return "Mật khẩu phải gồm cả chữ và số"
    return None


def authenticate(conn, username: str, password: str) -> tuple[dict | None, str | None]:
    """Trả về (user, None) nếu đúng, (None, thông báo lỗi) nếu sai."""
    now = dt.datetime.utcnow()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user is None:
        check_password_hash(_DUMMY_HASH, password)
        return None, "Sai tên đăng nhập hoặc mật khẩu"

    if user["locked_until"] and dt.datetime.fromisoformat(user["locked_until"]) > now:
        remain = int((dt.datetime.fromisoformat(user["locked_until"]) - now).total_seconds() // 60) + 1
        return None, f"Tài khoản tạm khóa do đăng nhập sai nhiều lần. Thử lại sau {remain} phút"

    if check_password_hash(user["password_hash"], password):
        conn.execute("UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE id = ?", (user["id"],))
        conn.commit()
        return dict(user), None

    failed = user["failed_attempts"] + 1
    locked = None
    if failed >= MAX_FAILED:
        locked = (now + dt.timedelta(minutes=LOCK_MINUTES)).isoformat()
        failed = 0
    conn.execute("UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id = ?",
                 (failed, locked, user["id"]))
    conn.commit()
    if locked:
        audit(conn, "account_locked", f"Khóa tài khoản {username} {LOCK_MINUTES} phút", username=username)
        return None, f"Sai mật khẩu {MAX_FAILED} lần. Tài khoản bị khóa {LOCK_MINUTES} phút"
    return None, "Sai tên đăng nhập hoặc mật khẩu"


def audit(conn, action: str, detail: str = "", username: str | None = None) -> None:
    user = username or (g.user["username"] if getattr(g, "user", None) else None)
    ip = request.remote_addr if request else None
    conn.execute("INSERT INTO audit_log(username, ip, action, detail) VALUES (?,?,?,?)",
                 (user, ip, action, detail[:1000]))
    conn.commit()


# ----- CSRF
def csrf_token() -> str:
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_urlsafe(32)
    return session["_csrf"]


def check_csrf() -> None:
    if request.method == "POST":
        sent = request.form.get("_csrf", "")
        if not sent or not hmac.compare_digest(sent, session.get("_csrf", "")):
            abort(400, "CSRF token không hợp lệ")


# ----- Phân quyền
def login_required(view):
    @wraps(view)
    def wrapped(*a, **kw):
        if g.user is None:
            return redirect(url_for("login", next=request.path))
        return view(*a, **kw)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*a, **kw):
        if g.user is None:
            return redirect(url_for("login"))
        if g.user["role"] != "admin":
            flash("Chức năng này chỉ dành cho quản trị viên", "error")
            return redirect(url_for("dashboard"))
        return view(*a, **kw)
    return wrapped


def security_headers(resp):
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; "
        "frame-ancestors 'none'; form-action 'self'; base-uri 'none'")
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "no-referrer"
    return resp
