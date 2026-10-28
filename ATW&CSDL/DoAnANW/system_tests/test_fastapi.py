
from fastapi.testclient import TestClient
from python_app.main import app

client = TestClient(app)

def test_routes():
    res = client.get("/api/health")
    assert res.status_code == 200
    print("Health response:", res.json())

    res_stats = client.get("/api/fraud/statistics")
    assert res_stats.status_code == 200
    print("Statistics response:", res_stats.json())

    res_sim = client.post("/api/fraud/simulation", json={"scenario": "ACCOUNT_TAKEOVER"})
    assert res_sim.status_code == 200
    data = res_sim.json()
    print("Simulation analysis keys:", data["analysis"].keys())
    print("Simulation Risk Score:", data["analysis"].get("riskScore") or data["analysis"].get("risk_score"))

if __name__ == "__main__":
    test_routes()
    print("All FastAPI endpoints verified successfully!")

