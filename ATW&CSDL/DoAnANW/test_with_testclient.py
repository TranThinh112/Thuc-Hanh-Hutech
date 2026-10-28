from fastapi.testclient import TestClient
from python_app.main import app

client = TestClient(app, raise_server_exceptions=True)

try:
    resp = client.post("/api/transactions", json={
        "amount": 300000,
        "paymentMethod": "MOMO",
        "locationCity": "Hà Nội",
        "ipAddress": "113.161.44.12",
        "deviceId": "device_thinh_iphone",
        "scenarioTag": "legit"
    })
    print("TestClient status:", resp.status_code, resp.json().get("status"))
except Exception as e:
    import traceback
    traceback.print_exc()
