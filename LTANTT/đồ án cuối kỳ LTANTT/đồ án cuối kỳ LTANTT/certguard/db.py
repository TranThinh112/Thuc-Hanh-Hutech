"""Lớp truy cập CSDL SQLite. Mọi câu lệnh đều dùng tham số (?) để chống SQL Injection."""
import json
import sqlite3
from pathlib import Path

from flask import g

DB_PATH = Path(__file__).resolve().parent / "instance" / "certguard.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT UNIQUE NOT NULL,
    password_hash   TEXT NOT NULL,
    role            TEXT NOT NULL DEFAULT 'user',      -- admin | user
    failed_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until    TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS domains (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    host        TEXT NOT NULL,
    port        INTEGER NOT NULL DEFAULT 443,
    label       TEXT,
    enabled     INTEGER NOT NULL DEFAULT 1,
    created_by  TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(host, port)
);
CREATE TABLE IF NOT EXISTS scans (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id    INTEGER REFERENCES domains(id) ON DELETE CASCADE,
    host         TEXT NOT NULL,
    port         INTEGER NOT NULL,
    scanned_at   TEXT NOT NULL,
    status       TEXT NOT NULL,            -- ok | warning | error | unreachable
    grade        TEXT,
    days_left    REAL,
    not_after    TEXT,
    fingerprint  TEXT,
    error        TEXT,
    triggered_by TEXT NOT NULL,            -- manual | schedule | quick
    result_json  TEXT
);
CREATE INDEX IF NOT EXISTS idx_scans_domain ON scans(domain_id, scanned_at DESC);
CREATE TABLE IF NOT EXISTS alerts (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id  INTEGER REFERENCES domains(id) ON DELETE CASCADE,
    scan_id    INTEGER,
    level      TEXT NOT NULL,
    message    TEXT NOT NULL,
    channel    TEXT NOT NULL,
    success    INTEGER NOT NULL,
    detail     TEXT,
    sent_at    TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS audit_log (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ts        TEXT NOT NULL DEFAULT (datetime('now')),
    username  TEXT,
    ip        TEXT,
    action    TEXT NOT NULL,
    detail    TEXT
);
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

DEFAULT_SETTINGS = {
    "warn_days": "30",
    "critical_days": "7",
    "scan_interval_minutes": "1440",   # 1 ngày; khi demo có thể đặt 2-5 phút
    "alert_cooldown_minutes": "60",
    "allowlist": "*.certguard.webservers",
}


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(path: Path = DB_PATH) -> None:
    with connect(path) as conn:
        conn.executescript(SCHEMA)
        for k, v in DEFAULT_SETTINGS.items():
            conn.execute("INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)", (k, v))


def get_db() -> sqlite3.Connection:
    """Mỗi request dùng một kết nối riêng, đóng ở teardown."""
    if "db" not in g:
        g.db = connect()
    return g.db


def close_db(_=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# ----- settings
def get_settings(conn) -> dict:
    return {r["key"]: r["value"] for r in conn.execute("SELECT key, value FROM settings")}


def set_setting(conn, key, value):
    conn.execute("INSERT INTO settings(key, value) VALUES (?, ?) "
                 "ON CONFLICT(key) DO UPDATE SET value = excluded.value", (key, str(value)))
    conn.commit()


# ----- scans
def save_scan(conn, domain_id, host, port, triggered_by, result=None, error=None) -> int:
    if result:
        leaf = result["leaf"]
        stored = json.dumps(result, ensure_ascii=False)
        cur = conn.execute(
            "INSERT INTO scans(domain_id, host, port, scanned_at, status, grade, days_left, not_after, "
            "fingerprint, triggered_by, result_json) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (domain_id, host, port, result["scanned_at"], result["status"], result["grade"],
             result["days_left"], leaf["not_after"], leaf["sha256"], triggered_by, stored))
    else:
        cur = conn.execute(
            "INSERT INTO scans(domain_id, host, port, scanned_at, status, error, triggered_by) "
            "VALUES (?,?,?,datetime('now'),'unreachable',?,?)",
            (domain_id, host, port, error, triggered_by))
    conn.commit()
    return cur.lastrowid


def latest_scans(conn):
    """Danh sách domain kèm kết quả quét gần nhất."""
    return conn.execute("""
        SELECT d.*, s.id AS scan_id, s.status, s.grade, s.days_left, s.not_after, s.scanned_at, s.error
        FROM domains d
        LEFT JOIN scans s ON s.id = (SELECT id FROM scans WHERE domain_id = d.id ORDER BY id DESC LIMIT 1)
        ORDER BY CASE s.status WHEN 'error' THEN 0 WHEN 'unreachable' THEN 1 WHEN 'warning' THEN 2
                               WHEN 'ok' THEN 3 ELSE 4 END, s.days_left
    """).fetchall()


def load_result(row):
    return json.loads(row["result_json"]) if row and row["result_json"] else None
