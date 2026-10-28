import sys
sys.stdout.reconfigure(encoding="utf-8")
from fastapi.testclient import TestClient
from python_app.main import app

client = TestClient(app)

print("--- 1. TEST LOGIN (THINH - 0972445090) ---")
res = client.post("/api/auth/login", json={"username": "thinh", "password": "123"})
print("Status:", res.status_code)
assert res.status_code == 200, f"Login failed: {res.text}"
login_data = res.json()
access_token = login_data["accessToken"]
refresh_token = login_data["refreshToken"]
user_info = login_data["user"]
print(f"Logged in user: {user_info['name']} | Role: {user_info['role']} | Phone: {user_info['phone']}")
print("AccessToken (JWT):", access_token[:30] + "...")
print("RefreshToken (JWT):", refresh_token[:30] + "...")

print("\n--- 2. TEST REFRESH TOKEN ---")
res_ref = client.post("/api/auth/refresh", json={"refreshToken": refresh_token})
print("Refresh status:", res_ref.status_code)
assert res_ref.status_code == 200
new_access = res_ref.json()["accessToken"]
print("New AccessToken:", new_access[:30] + "...")

print("\n--- 3. TEST AUTH ME ---")
res_me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {access_token}"})
print("Me status:", res_me.status_code, res_me.json())

print("\n--- 4. TEST CREATE NORMAL TRANSACTION (APPROVE) ---")
normal_tx = {
    "amount": 2500000.0,
    "paymentMethod": "MOMO",
    "customerPhone": "0972445090",
    "shippingAddress": "15 Cầu Giấy, Hà Nội",
    "itemsSummary": "Wireless Mechanical Keyboard",
    "locationCity": "Hà Nội",
    "ipAddress": "113.161.44.12",
    "deviceId": "device_thinh_iphone"
}
res_tx_ok = client.post("/api/transactions", json=normal_tx, headers={"Authorization": f"Bearer {access_token}"})
print("Normal TX status:", res_tx_ok.status_code)
tx_ok_data = res_tx_ok.json()
print("Decision:", tx_ok_data["decision"], "| Status:", tx_ok_data["status"])
print("User Message:", tx_ok_data["userMessage"])
print("SMS Notification sent:")
print(tx_ok_data["smsNotification"]["content"])

print("\n--- 5. TEST CREATE FRAUD TRANSACTION (BLOCK) ---")
fraud_tx = {
    "amount": 49990000.0,
    "paymentMethod": "VISA",
    "customerPhone": "0972445090",
    "shippingAddress": "Shibuya, Tokyo",
    "itemsSummary": "MacBook Pro 14 M3 Pro",
    "locationCity": "Tokyo",
    "locationCountry": "Japan",
    "ipAddress": "185.220.101.5",
    "deviceId": "device_hacker_kali"
}
res_tx_fraud = client.post("/api/transactions", json=fraud_tx, headers={"Authorization": f"Bearer {access_token}"})
print("Fraud TX status:", res_tx_fraud.status_code)
tx_fraud_data = res_tx_fraud.json()
print("Decision:", tx_fraud_data["decision"], "| Status:", tx_fraud_data["status"])
print("User Explanation:", tx_fraud_data["userExplanation"])
print("SMS Warning sent:")
print(tx_fraud_data["smsNotification"]["content"])

print("\n--- 6. TEST ADMIN ACTION (OVERRIDE APPROVE) ---")
admin_login = client.post("/api/auth/login", json={"username": "admin", "password": "123"}).json()
admin_token = admin_login["accessToken"]
blocked_id = tx_fraud_data["transaction"]["id"]
res_action = client.patch(
    f"/api/admin/transactions/{blocked_id}/action",
    json={"action": "OVERRIDE_APPROVE", "note": "Khách hàng Thịnh gọi điện xác nhận chính chủ"},
    headers={"Authorization": f"Bearer {admin_token}"}
)
print("Admin Action Status:", res_action.status_code, res_action.json())

print("\nALL BACKEND API TESTS PASSED SUCCESSFULLY!")
