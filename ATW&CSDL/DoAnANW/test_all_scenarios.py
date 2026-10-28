from fastapi.testclient import TestClient
from python_app.main import app

client = TestClient(app, raise_server_exceptions=True)

# Unlock first to be clean
client.post("/api/user/emergency-unlock", json={})

scenarios = [
    ("LEGIT", {"amount": 500000, "paymentMethod": "VISA", "locationCity": "Hà Nội", "ipAddress": "113.161.44.12", "deviceId": "device_windows_pc", "scenarioTag": "legit"}),
    ("HIGH_AMOUNT", {"amount": 68000000, "paymentMethod": "VISA", "locationCity": "Hà Nội", "ipAddress": "113.161.44.12", "deviceId": "device_windows_pc", "scenarioTag": "high_amount"}),
    ("VELOCITY", {"amount": 2000000, "paymentMethod": "VISA", "locationCity": "Hà Nội", "ipAddress": "113.161.44.12", "deviceId": "device_windows_pc", "scenarioTag": "velocity"}),
    ("ATO", {"amount": 45000000, "paymentMethod": "VISA", "locationCity": "Tokyo", "ipAddress": "185.220.101.5", "deviceId": "device_hacker_kali", "scenarioTag": "ato"}),
    ("TRAVEL", {"amount": 2500000, "paymentMethod": "MASTERCARD", "locationCity": "London", "ipAddress": "45.142.120.10", "deviceId": "device_windows_pc", "scenarioTag": "travel"}),
    ("CARD_TESTING", {"amount": 99000, "paymentMethod": "JCB", "locationCity": "TP. Hồ Chí Minh", "ipAddress": "45.33.32.156", "deviceId": "device_bot_tester_01", "scenarioTag": "card_testing"})
]

for name, payload in scenarios:
    r = client.post("/api/transactions", json=payload)
    data = r.json()
    st = data.get("status")
    dec = data.get("decision")
    otp_req = data.get("requiresOtp")
    score = data.get("fraudAnalysis", {}).get("riskScore")
    otp_val = data.get("otpCode")
    tx_id = data.get("transaction", {}).get("id")
    print(f"[{name:12}] => Status: {st:8} | Decision: {dec:7} | Score: {score:3} | RequiresOTP: {str(otp_req):5} | OTP: {otp_val}")

    if otp_req and tx_id and otp_val:
        # Test verify OTP
        v_res = client.post(f"/api/transactions/{tx_id}/verify-otp", json={"otp": otp_val})
        v_data = v_res.json()
        print(f"   ↳ [OTP Verification]: {v_data.get('status')} - {v_data.get('message')[:50]}...")
