# -*- coding: utf-8 -*-
import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from python_app.main import app

client = TestClient(app)

print("=" * 60)
print("RUNNING COMPREHENSIVE E-COMMERCE FRAUD DETECTION SYSTEM AUDIT")
print("=" * 60)

# 1. Health check
res = client.get("/api/health")
assert res.status_code == 200, "Health check failed"
print("✓ 1. API Health Check OK:", res.json()["status"])

# 2. Client Info Auto-Detection
res = client.get("/api/client-info", headers={
    "X-Forwarded-For": "14.161.42.88",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X)"
})
assert res.status_code == 200, "Client-info failed"
c_data = res.json()
print("✓ 2. Client Info Auto-Detection OK:")
print(f"     Detected IP: {c_data['detectedIp']} (Public: {c_data['isPublicIp']})")
print(f"     Device: {c_data['deviceId']} ({c_data['deviceName']})")
print(f"     Geo Location: {c_data['city']}, {c_data['country']}")
assert c_data["detectedIp"] == "14.161.42.88"
assert c_data["deviceId"] == "device_apple_ios"

# 3. Authentication (User & Admin)
res_thinh = client.post("/api/auth/login", json={"username": "thinh", "password": "123"})
assert res_thinh.status_code == 200, "Login thinh failed"
thinh_token = res_thinh.json()["accessToken"]
print("✓ 3. Login Customer 'thinh' (Role: USER) OK - Token generated")

res_admin = client.post("/api/auth/login", json={"username": "admin", "password": "123"})
assert res_admin.status_code == 200, "Login admin failed"
admin_token = res_admin.json()["accessToken"]
print("✓ 4. Login 'admin' (Role: ADMIN) OK - Token generated")

# 4. RBAC Check (USER cannot access admin routes)
res_unauth = client.get("/api/fraud/transactions", headers={"Authorization": f"Bearer {thinh_token}"})
assert res_unauth.status_code == 403, "RBAC protection failed!"
print("✓ 5. RBAC Protection OK: USER role cannot access /api/fraud/transactions (HTTP 403 Forbidden)")

res_auth = client.get("/api/fraud/transactions", headers={"Authorization": f"Bearer {admin_token}"})
assert res_auth.status_code == 200, "Admin access failed!"
print(f"✓ 6. Admin Access OK: Retrieved {len(res_auth.json())} transactions from audit DB")

# 5. Normal Order Creation with Auto-Extracted IP
order_normal = client.post("/api/transactions", json={
    "amount": 2500000,
    "paymentMethod": "MOMO",
    "customerPhone": "0972445090",
    "shippingAddress": "Số 15 Cầu Giấy, Hà Nội",
    "itemsSummary": "Wireless Mechanical Keyboard",
    "locationCity": "Hà Nội"
}, headers={
    "Authorization": f"Bearer {thinh_token}",
    "X-Forwarded-For": "113.161.44.12",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})
assert order_normal.status_code == 200
norm_tx = order_normal.json()
print("✓ 7. Normal Order Flow OK:")
print(f"     Status: {norm_tx['status']} | Decision: {norm_tx['decision']}")
print(f"     SMS Notification: {norm_tx.get('smsNotification', {}).get('content')}")

# 6. Fraud Scenario: Impossible Travel (Tokyo Tor exit node / Kali hacker within minutes)
order_fraud = client.post("/api/transactions", json={
    "amount": 35000000,
    "paymentMethod": "VISA",
    "customerPhone": "0972445090",
    "shippingAddress": "Shibuya, Tokyo, Japan",
    "itemsSummary": "iPhone 16 Pro Max 256GB",
    "ipAddress": "185.220.101.5",
    "deviceId": "device_hacker_kali",
    "locationCity": "Tokyo"
}, headers={
    "Authorization": f"Bearer {thinh_token}",
    "X-Forwarded-For": "185.220.101.5",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Kali/2026"
})
assert order_fraud.status_code == 200
fraud_tx = order_fraud.json()
print("✓ 8. Fraud Attack Scenario (Impossible Travel + Hacker Kali) OK:")
print(f"     Status: {fraud_tx['status']} | Decision: {fraud_tx['decision']}")
print(f"     Risk Score: {fraud_tx['fraudAnalysis']['riskScore']} ({fraud_tx['fraudAnalysis']['riskLevel']})")
print(f"     User Explanation: {fraud_tx.get('userExplanation')}")
print(f"     SMS Alert Sent: {fraud_tx.get('smsNotification', {}).get('content')}")
assert fraud_tx['decision'] == 'BLOCK', "Fraud transaction should have been BLOCKED!"

# 7. Check Admin Audit Trail for Block Reason and Customer Details
res_alerts = client.get("/api/fraud/alerts", headers={"Authorization": f"Bearer {admin_token}"})
assert res_alerts.status_code == 200
alerts = res_alerts.json()
print(f"✓ 9. Admin Alerts & Audit Trail OK: {len(alerts)} alerts currently logged.")
latest_alert = alerts[0]
print(f"     Latest Alert: {latest_alert['title']}")
print(f"     Description: {latest_alert['description']}")

# 8. Verify Railway Files
files = ["Procfile", "requirements.txt", "railway.json", "runtime.txt", "Dockerfile", ".env.example"]
for f in files:
    assert os.path.exists(f), f"Missing deployment file: {f}"
print(f"✓ 10. Railway Production Files Verified: {', '.join(files)}")

print("=" * 60)
print("ALL 10/10 SYSTEM VERIFICATION TESTS PASSED SUCCESSFULLY!")
print("=" * 60)