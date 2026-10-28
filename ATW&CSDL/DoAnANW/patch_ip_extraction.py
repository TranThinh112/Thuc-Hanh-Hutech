with open("python_app/main.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add Request to imports
text = text.replace(
    'from fastapi import FastAPI, Depends, HTTPException, Query, Body',
    'from fastapi import FastAPI, Depends, HTTPException, Query, Body, Request'
)

# 2. Update create_transaction_api to accept request: Request and extract real IP & User-Agent
old_def = """@app.post("/api/transactions")
def create_transaction_api(
    payload: Dict[str, Any] = Body(...),
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):"""

new_def = """@app.post("/api/transactions")
def create_transaction_api(
    request: Request,
    payload: Dict[str, Any] = Body(...),
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):"""

text = text.replace(old_def, new_def)

# 3. Enhance IP and device extraction logic to auto-extract from Request headers (X-Forwarded-For, X-Real-IP, Client Host)
old_ip_extraction = """    amount = float(payload.get("amount", 0))
    payment_method = str(payload.get("paymentMethod", "VISA"))
    ip_address = str(payload.get("ipAddress", "113.161.44.12"))
    device_id = str(payload.get("deviceId", "device_user_phone"))
    user_agent = str(payload.get("userAgent", "Mozilla/5.0 Client"))
    city = str(payload.get("locationCity", "Hà Nội"))
    country = str(payload.get("locationCountry", "Vietnam"))
    shipping_address = str(payload.get("shippingAddress", "Số 15 Cầu Giấy, Hà Nội"))
    items_summary = str(payload.get("itemsSummary", "Sản phẩm công nghệ"))
    customer_phone = str(payload.get("customerPhone", ""))"""

new_ip_extraction = """    amount = float(payload.get("amount", 0))
    payment_method = str(payload.get("paymentMethod", "VISA"))
    shipping_address = str(payload.get("shippingAddress", "Số 15 Cầu Giấy, Hà Nội"))
    items_summary = str(payload.get("itemsSummary", "Sản phẩm công nghệ"))
    customer_phone = str(payload.get("customerPhone", ""))

    # TU DONG TRICH XUAT IP THAT TU PACKET MANG HOAC PROXY (Railway / Cloudflare / Nginx)
    forwarded_for = request.headers.get("x-forwarded-for")
    real_ip = request.headers.get("x-real-ip")
    client_host = request.client.host if request.client else "127.0.0.1"

    if forwarded_for:
        detected_real_ip = forwarded_for.split(",")[0].strip()
    elif real_ip:
        detected_real_ip = real_ip.strip()
    else:
        detected_real_ip = client_host

    # Neu nguoi dung co override bang preset kiem thu (Tokyo / London / Kali) thi uu tien
    requested_ip = payload.get("ipAddress")
    if requested_ip and requested_ip not in ["113.161.44.12", "127.0.0.1", "localhost"]:
        ip_address = str(requested_ip)
    elif detected_real_ip not in ["127.0.0.1", "localhost", "::1"]:
        ip_address = detected_real_ip
    else:
        ip_address = str(payload.get("ipAddress", "113.161.44.12"))

    # Tu dong trich xuat User-Agent & Device ID thuc te
    real_user_agent = request.headers.get("user-agent", "Mozilla/5.0 Client")
    user_agent = payload.get("userAgent") or real_user_agent

    requested_device = payload.get("deviceId")
    if requested_device and "hacker" in requested_device or "script" in requested_device or "foreign" in requested_device:
        device_id = requested_device
    else:
        # Tu dong gan nhan thiet bi theo trinh duyet thuc te (iPhone, Android, Windows, Mac)
        ua_lower = real_user_agent.lower()
        if "iphone" in ua_lower or "ipad" in ua_lower:
            detected_dev = "device_apple_ios"
        elif "android" in ua_lower:
            detected_dev = "device_android_mobile"
        elif "macintosh" in ua_lower:
            detected_dev = "device_apple_macos"
        else:
            detected_dev = "device_windows_pc"
        device_id = requested_device if requested_device and requested_device != "device_user_phone" else detected_dev

    city = str(payload.get("locationCity", "Hà Nội"))
    country = str(payload.get("locationCountry", "Vietnam"))"""

text = text.replace(old_ip_extraction, new_ip_extraction)

with open("python_app/main.py", "w", encoding="utf-8") as f:
    f.write(text)

print("python_app/main.py updated with auto real IP & device extraction!")
