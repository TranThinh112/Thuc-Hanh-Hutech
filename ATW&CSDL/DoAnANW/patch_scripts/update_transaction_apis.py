with open("python_app/main.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Replace get_transactions
old_get_tx_start = '@app.get("/api/fraud/transactions")\ndef get_transactions('
old_get_tx_end = '@app.get("/api/fraud/transactions/{id}")'

idx_start = text.find(old_get_tx_start)
idx_end = text.find(old_get_tx_end)

new_get_transactions = """@app.get("/api/fraud/transactions")
def get_transactions(
    riskLevel: Optional[str] = Query(None),
    decision: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Transaction)
    if search:
        query = query.filter(
            models.Transaction.id.like(f"%{search}%")
            | models.Transaction.user_id.like(f"%{search}%")
            | models.Transaction.ip_address.like(f"%{search}%")
            | models.Transaction.device_id.like(f"%{search}%")
        )

    txs = query.order_by(models.Transaction.created_at.desc()).limit(150).all()

    result = []
    for t in txs:
        fa = t.fraud_analysis
        if riskLevel and (not fa or fa.risk_level != riskLevel):
            continue
        if decision and (not fa or fa.decision != decision):
            continue
        if status_filter and t.status != status_filter:
            continue

        triggered_rules_list = []
        if fa and fa.rule_results:
            for rr in fa.rule_results:
                triggered_rules_list.append({
                    "ruleId": rr.rule_id,
                    "ruleName": rr.rule_name,
                    "score": rr.score,
                    "severity": rr.severity,
                    "reason": rr.reason,
                })

        item = {
            "id": t.id,
            "shortId": "#TX-" + t.id[:8].upper(),
            "userId": t.user_id,
            "userName": t.user.name if t.user else "Khách vãng lai",
            "userPhone": t.user.phone if t.user else "Chưa có",
            "userUsername": t.user.username if t.user else "",
            "itemsSummary": t.items_summary or "Sản phẩm công nghệ",
            "shippingAddress": t.shipping_address or "Việt Nam",
            "amount": t.amount,
            "currency": t.currency,
            "paymentMethod": t.payment_method,
            "status": t.status,
            "adminAction": t.admin_action,
            "adminActionNote": t.admin_action_note,
            "ipAddress": t.ip_address,
            "deviceId": t.device_id,
            "userAgent": t.user_agent,
            "locationCity": t.location_city,
            "locationCountry": t.location_country,
            "createdAt": t.created_at.strftime("%H:%M:%S %d/%m/%Y"),
            "user": {
                "name": t.user.name,
                "phone": t.user.phone,
                "email": t.user.email,
                "username": t.user.username,
                "role": t.user.role,
            } if t.user else None,
            "fraudAnalysis": {
                "riskScore": fa.risk_score if fa else 0,
                "riskLevel": fa.risk_level if fa else "LOW",
                "decision": fa.decision if fa else t.status,
                "explanation": fa.explanation if fa else "Không có giải trình",
                "triggeredRules": triggered_rules_list,
            } if fa else None,
        }
        result.append(item)

    return result

"""

text = text[:idx_start] + new_get_transactions + text[idx_end:]

# 2. Add admin_transaction_action right before @app.get("/api/fraud/alerts")
old_alerts_start = '@app.get("/api/fraud/alerts")'
idx_alerts = text.find(old_alerts_start)

admin_action_endpoint = """@app.patch("/api/admin/transactions/{tx_id}/action")
def admin_transaction_action(
    tx_id: str,
    payload: Dict[str, Any] = Body(...),
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    action = payload.get("action")  # "OVERRIDE_APPROVE" | "CONFIRM_BLOCK"
    note = str(payload.get("note", ""))

    tx = db.query(models.Transaction).filter_by(id=tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Không tìm thấy giao dịch")

    tx.admin_action = action
    tx.admin_action_note = note
    if action == "OVERRIDE_APPROVE":
        tx.status = "APPROVED"
        alerts = db.query(models.FraudAlert).filter_by(transaction_id=tx_id).all()
        for a in alerts:
            a.status = "RESOLVED_LEGIT"
            a.description += f" [Admin đã mở khóa & duyệt lúc {datetime.now().strftime('%H:%M %d/%m')}]"

        sms_body = f"[ECOMMERCE SECURE PAY] Đơn hàng #{tx.id[:8].upper()} trị giá {tx.amount:,.0f} VND đã được Quản trị viên thẩm định và MỞ KHÓA DUYỆT THÀNH CÔNG. Đơn hàng đang được chuẩn bị giao. Hotline hỗ trợ: 1900-8888."
        db.add(models.SmsNotification(
            user_id=tx.user_id,
            phone=tx.user.phone if tx.user else "0972445090",
            order_id=tx.id,
            message_type="ORDER_SUCCESS",
            content=sms_body,
            status="SENT"
        ))
    elif action == "CONFIRM_BLOCK":
        tx.status = "BLOCKED"
        alerts = db.query(models.FraudAlert).filter_by(transaction_id=tx_id).all()
        for a in alerts:
            a.status = "RESOLVED_FRAUD"
            a.description += f" [Admin đã xác nhận chặn gian lận lúc {datetime.now().strftime('%H:%M %d/%m')}]"

    db.commit()
    return {
        "message": "Thao tác thành công",
        "status": tx.status,
        "adminAction": tx.admin_action,
        "transactionId": tx.id
    }

"""

if "/api/admin/transactions/{tx_id}/action" not in text:
    text = text[:idx_alerts] + admin_action_endpoint + text[idx_alerts:]

with open("python_app/main.py", "w", encoding="utf-8") as f:
    f.write(text)

print("get_transactions and admin_transaction_action updated!")
