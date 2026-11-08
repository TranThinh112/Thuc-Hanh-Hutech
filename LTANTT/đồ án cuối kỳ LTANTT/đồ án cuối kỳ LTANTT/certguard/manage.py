"""
Công cụ quản trị dòng lệnh.

    python manage.py create-admin     Tạo tài khoản quản trị (nhập mật khẩu ẩn)
    python manage.py reset-db         XÓA toàn bộ CSDL và tạo lại bảng trống
    python manage.py stats            Thống kê nhanh số bản ghi trong CSDL
"""
import getpass
import sys

import db
import security


def create_admin():
    db.init_db()
    username = input("Tên đăng nhập admin: ").strip()
    while True:
        pw = getpass.getpass("Mật khẩu (ẩn khi gõ): ")
        err = security.password_policy(pw)
        if err:
            print(" -", err)
            continue
        if pw != getpass.getpass("Nhập lại mật khẩu: "):
            print(" - Không khớp")
            continue
        break
    conn = db.connect()
    try:
        conn.execute("INSERT INTO users(username, password_hash, role) VALUES (?,?, 'admin')",
                     (username, security.hash_password(pw)))
        conn.commit()
        print(f"Đã tạo admin '{username}'")
    except db.sqlite3.IntegrityError:
        print("Tên đăng nhập đã tồn tại")


def reset_db():
    if input("Xóa toàn bộ dữ liệu? Gõ 'yes' để xác nhận: ") != "yes":
        return
    db.DB_PATH.unlink(missing_ok=True)
    db.init_db()
    print("Đã tạo lại CSDL trống. Nhớ chạy lại: python manage.py create-admin")


def stats():
    db.init_db()
    conn = db.connect()
    for t in ("users", "domains", "scans", "alerts", "audit_log"):
        print(f"{t:<10} {conn.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]:>6} bản ghi")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    {"create-admin": create_admin, "reset-db": reset_db, "stats": stats}.get(cmd, lambda: print(__doc__))()
