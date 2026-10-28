# -*- coding: utf-8 -*-
with open("python_app/main.py", "r", encoding="utf-8") as f:
    text = f.read()

# Protect /api/fraud/transactions
old_get_tx = """@app.get("/api/fraud/transactions")
def get_transactions(
    riskLevel: Optional[str] = Query(None),
    decision: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):"""

new_get_tx = """@app.get("/api/fraud/transactions")
def get_transactions(
    riskLevel: Optional[str] = Query(None),
    decision: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    current_admin: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):"""

if old_get_tx in text:
    text = text.replace(old_get_tx, new_get_tx)
    print("Protected /api/fraud/transactions with require_admin")

# Protect /api/fraud/alerts
old_alerts = """@app.get("/api/fraud/alerts")
def get_alerts(status: Optional[str] = Query(None), db: Session = Depends(get_db)):"""

new_alerts = """@app.get("/api/fraud/alerts")
def get_alerts(status: Optional[str] = Query(None), current_admin: models.User = Depends(require_admin), db: Session = Depends(get_db)):"""

if old_alerts in text:
    text = text.replace(old_alerts, new_alerts)
    print("Protected /api/fraud/alerts with require_admin")

# Protect /api/fraud/statistics
old_stats = """@app.get("/api/fraud/statistics")
def get_statistics(db: Session = Depends(get_db)):"""

new_stats = """@app.get("/api/fraud/statistics")
def get_statistics(current_admin: models.User = Depends(require_admin), db: Session = Depends(get_db)):"""

if old_stats in text:
    text = text.replace(old_stats, new_stats)
    print("Protected /api/fraud/statistics with require_admin")

with open("python_app/main.py", "w", encoding="utf-8") as f:
    f.write(text)

print("python_app/main.py RBAC applied!")