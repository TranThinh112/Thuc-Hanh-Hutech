import sys
sys.stdout.reconfigure(encoding="utf-8")
import urllib.request, json

# 1. Login
req_l = urllib.request.Request("http://127.0.0.1:8000/api/auth/login", data=json.dumps({"username": "thinh", "password": "123"}).encode("utf-8"), headers={"Content-Type": "application/json"})
token = json.loads(urllib.request.urlopen(req_l).read().decode())["accessToken"]

# 2. Test request with X-Forwarded-For (simulating Railway / Public Cloud traffic)
p = {
    "amount": 2500000.0,
    "paymentMethod": "MOMO",
    "customerPhone": "0972445090",
    "shippingAddress": "Quận 1, TP. Hồ Chí Minh",
    "itemsSummary": "Wireless Mechanical Keyboard",
    "locationCity": "Hồ Chí Minh"
}
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/transactions",
    data=json.dumps(p).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "X-Forwarded-For": "14.161.42.88",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X)"
    }
)
res = json.loads(urllib.request.urlopen(req).read().decode())
print("Transaction ID:", res["transaction"]["id"])
print("Detected IP in Transaction:", res["transaction"]["ipAddress"])
print("Detected Device in Transaction:", res["transaction"]["deviceId"])
assert res["transaction"]["ipAddress"] == "14.161.42.88", f"IP extraction failed: {res['transaction']['ipAddress']}"
assert res["transaction"]["deviceId"] == "device_apple_ios", f"Device extraction failed: {res['transaction']['deviceId']}"
print("TEST SUCCESS: Backend automatically extracted Real IP from X-Forwarded-For and User-Agent device!")
