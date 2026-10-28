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
        print(f"   Reason: {data.get('userExplanation')[:100]}...")
        return data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        print(f"[{name}] HTTP {e.code} - Body: {body[:150]}")
        return None

test_tx("High Amount", {
    "amount": 25000000,
    "paymentMethod": "VISA",
    "locationCity": "Hà Nội",
    "ipAddress": "113.161.44.12",
    "deviceId": "device_thinh_iphone",
    "scenarioTag": "high_amount"
})

test_tx("Impossible Travel", {
    "amount": 1500000,
    "paymentMethod": "VISA",
    "locationCity": "Tokyo",
    "ipAddress": "185.220.101.5",
    "deviceId": "device_hacker_kali",
    "scenarioTag": "impossible_travel"
})

test_tx("Normal Transaction", {
    "amount": 300000,
    "paymentMethod": "MOMO",
    "locationCity": "Hà Nội",
    "ipAddress": "113.161.44.12",
    "deviceId": "device_thinh_iphone",
    "scenarioTag": "legit"
})
