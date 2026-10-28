import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

def test_tx(name, payload):
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/transactions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode("utf-8"))
        print(f"[{name}] HTTP {resp.status} - Status: {data.get('status')} - Decision: {data.get('decision')}")
        print(f"   Message: {data.get('userMessage')}")
        return data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        print(f"[{name}] HTTP {e.code} - Body: {body[:150]}")
        return None

# Test Normal transaction with Thịnh (who has past transactions seeded)
test_tx("1. Giao dịch hợp lệ (Legit)", {
    "amount": 300000,
    "paymentMethod": "MOMO",
    "locationCity": "Hà Nội",
    "ipAddress": "113.161.44.12",
    "deviceId": "device_thinh_iphone",
    "username": "thinh",
    "scenarioTag": "legit"
})

# Test High Amount
test_tx("2. Đơn hàng giá trị cao", {
    "amount": 49990000,
    "paymentMethod": "VISA",
    "locationCity": "Hà Nội",
    "ipAddress": "113.161.44.12",
    "deviceId": "device_thinh_iphone",
    "username": "thinh",
    "scenarioTag": "high_amount"
})

# Test Impossible Travel
test_tx("3. Di chuyển bất khả thi (Tokyo)", {
    "amount": 1200000,
    "paymentMethod": "VISA",
    "locationCity": "Tokyo",
    "ipAddress": "185.220.101.5",
    "deviceId": "device_hacker_kali",
    "username": "thinh",
    "scenarioTag": "impossible_travel"
})
