"""
Gửi cảnh báo qua Telegram (và Email nếu cấu hình SMTP).

Thông tin bí mật (bot token, mật khẩu SMTP) được đọc từ biến môi trường / file .env,
KHÔNG lưu trong CSDL hay mã nguồn.
"""
import json
import os
import smtplib
import ssl
import urllib.parse
import urllib.request
from email.message import EmailMessage


def telegram_configured() -> bool:
    return bool(os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID"))


def email_configured() -> bool:
    return all(os.environ.get(k) for k in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "ALERT_EMAIL_TO"))


def send_telegram(text: str) -> tuple[bool, str]:
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat):
        return False, "Chưa cấu hình TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID"
    data = urllib.parse.urlencode({"chat_id": chat, "text": text, "parse_mode": "HTML",
                                   "disable_web_page_preview": "true"}).encode()
    try:
        # Kết nối tới Telegram có xác thực chứng thư đầy đủ (context mặc định)
        with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage",
                                    data=data, timeout=10, context=ssl.create_default_context()) as r:
            body = json.loads(r.read())
        return bool(body.get("ok")), "Đã gửi" if body.get("ok") else str(body)
    except Exception as e:
        return False, f"Lỗi gửi Telegram: {type(e).__name__}"  # không in token ra log


def send_email(subject: str, text: str) -> tuple[bool, str]:
    if not email_configured():
        return False, "Chưa cấu hình SMTP"
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = subject, os.environ["SMTP_USER"], os.environ["ALERT_EMAIL_TO"]
    msg.set_content(text)
    try:
        with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", 587)), timeout=15) as s:
            s.starttls(context=ssl.create_default_context())
            s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            s.send_message(msg)
        return True, "Đã gửi"
    except Exception as e:
        return False, f"Lỗi gửi email: {type(e).__name__}"


def notify(text_html: str, subject: str) -> list[tuple[str, bool, str]]:
    """Gửi qua mọi kênh đã cấu hình. Trả về [(kênh, thành công, chi tiết)]."""
    out = []
    if telegram_configured():
        out.append(("telegram", *send_telegram(text_html)))
    if email_configured():
        plain = (text_html.replace("<b>", "").replace("</b>", "")
                 .replace("<code>", "").replace("</code>", ""))
        out.append(("email", *send_email(subject, plain)))
    return out
