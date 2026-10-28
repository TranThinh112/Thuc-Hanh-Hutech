with open("python_app/main.py", "r", encoding="utf-8") as f:
    text = f.read()

old_start = '@app.post("/api/transactions")\ndef create_transaction_api('
old_end = '@app.get("/api/store/products")'

idx_start = text.find(old_start)
idx_end = text.find(old_end)

new_code = """def format_signals_for_user(signals: List[Any]) -> str:
    friendly_reasons = []
    for s in signals:
        rule = getattr(s, "rule", "")
        if "HIGH_AMOUNT" in rule:
            friendly_reasons.append("Giá trị đơn hàng cao vượt ngưỡng an toàn chi tiêu thông thường")
        elif "UNUSUAL_AMOUNT" in rule:
            friendly_reasons.append("Số tiền thanh toán tăng đột biến so với mức trung bình tài khoản")
        elif "LOCATION_CHANGE" in rule or "IMPOSSIBLE_TRAVEL" in rule:
            friendly_reasons.append("Vị trí đăng nhập thay đổi bất khả thi giữa hai địa điểm cách xa nhau trong tích tắc")
        elif "NEW_DEVICE" in rule:
            friendly_reasons.append("Thanh toán từ thiết bị lạ chưa từng được xác thực")
        elif "NEW_IP" in rule:
            friendly_reasons.append("Địa chỉ IP truy cập bất thường từ dải mạng chưa xác định")
        elif "TRANSACTION_VELOCITY" in rule or "VELOCITY" in rule:
            friendly_reasons.append("Tần suất tạo giao dịch dồn dập trong khoảng thời gian rất ngắn")
        elif "CARD_TESTING" in rule or "FAILED" in rule:
            friendly_reasons.append("Phát hiện chuỗi giao dịch thử thẻ liên tục với tỷ lệ thất bại cao")
        elif "ACCOUNT_TAKEOVER" in rule:
            friendly_reasons.append("Hệ sinh thái AI phát hiện dấu hiệu tài khoản có nguy cơ bị chiếm quyền (Account Takeover)")
        else:
            friendly_reasons.append(getattr(s, "reason", "Cảnh báo chỉ số rủi ro bảo mật"))
    return "; ".join(list(dict.fromkeys(friendly_reasons)))

@app.post("/api/transactions")
def create_transaction_api(
    payload: Dict[str, Any] = Body(...),
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    amount = float(payload.get("amount", 0))
    payment_method = str(payload.get("paymentMethod", "VISA"))
    ip_address = str(payload.get("ipAddress", "113.161.44.12"))
    device_id = str(payload.get("deviceId", "device_user_phone"))
    user_agent = str(payload.get("userAgent", "Mozilla/5.0 Client"))
    city = str(payload.get("locationCity", "Hà Nội"))
    country = str(payload.get("locationCountry", "Vietnam"))
    shipping_address = str(payload.get("shippingAddress", "Số 15 Cầu Giấy, Hà Nội"))
    items_summary = str(payload.get("itemsSummary", "Sản phẩm công nghệ"))
    customer_phone = str(payload.get("customerPhone", ""))

    # Xac dinh user
    user = current_user
    if not user:
        user_id_param = payload.get("userId")
        username_param = payload.get("username")
        if user_id_param:
            user = db.query(models.User).filter_by(id=user_id_param).first()
        elif username_param:
            user = db.query(models.User).filter(
                (models.User.username == username_param) | (models.User.phone == username_param)
            ).first()

    if not user:
        user = db.query(models.User).filter_by(username="thinh").first()
    if not user:
        user = db.query(models.User).first()

    phone_number = customer_phone or (user.phone if user else "0972445090")

    # Tao Transaction record
    tx = models.Transaction(
        user_id=user.id,
        amount=amount,
        currency="VND",
        payment_method=payment_method,
        status="PENDING",
        shipping_address=shipping_address,
        items_summary=items_summary,
        ip_address=ip_address,
        device_id=device_id,
        user_agent=user_agent,
        location_city=city,
        location_country=country,
        latitude=21.0285 if "Hà Nội" in city else (10.8231 if "Hồ Chí Minh" in city else 35.6762),
        longitude=105.8542 if "Hà Nội" in city else (106.6297 if "Hồ Chí Minh" in city else 139.6503),
    )
    db.add(tx)
    db.commit()

    ctx = build_context_from_db(tx.id, db)
    analysis = fraud_engine.analyze_transaction(ctx)

    feat_data = dict(
        amount_ratio=analysis.extracted_features.amount_ratio,
        transactions_last_1m=analysis.extracted_features.transactions_last_1m,
        transactions_last_5m=analysis.extracted_features.transactions_last_5m,
        transactions_last_15m=analysis.extracted_features.transactions_last_15m,
        transactions_last_1h=analysis.extracted_features.transactions_last_1h,
        failed_transactions_last_5m=analysis.extracted_features.failed_transactions_last_5m,
        different_payment_methods_15m=analysis.extracted_features.different_payment_methods_15m,
        different_devices_15m=analysis.extracted_features.different_devices_15m,
        different_ips_15m=analysis.extracted_features.different_ips_15m,
        is_new_device=analysis.extracted_features.is_new_device,
        is_new_ip=analysis.extracted_features.is_new_ip,
        location_changed=analysis.extracted_features.location_changed,
        distance_km=analysis.extracted_features.distance_km,
        time_diff_seconds=analysis.extracted_features.time_diff_seconds,
        impossible_travel=analysis.extracted_features.impossible_travel,
        account_age_hours=analysis.extracted_features.account_age_hours,
        failed_payment_rate=analysis.extracted_features.failed_payment_rate,
        feature_snapshot_json=analysis.extracted_features.model_dump_json(by_alias=True),
    )
    db.add(models.TransactionFeature(transaction_id=tx.id, **feat_data))

    fa = models.FraudAnalysis(
        transaction_id=tx.id,
        risk_score=analysis.risk_score,
        risk_level=analysis.risk_level,
        decision=analysis.decision,
        explanation=analysis.explanation,
    )
    db.add(fa)
    db.commit()

    for sig in analysis.signals:
        db.add(
            models.FraudRuleResult(
                fraud_analysis_id=fa.id,
                rule_id=sig.rule,
                rule_name=sig.rule,
                triggered=True,
                score=sig.score,
                severity=sig.severity,
                reason=sig.reason,
                evidence_json=json.dumps(sig.evidence),
            )
        )

    tx.status = "BLOCKED" if analysis.decision == "BLOCK" else "REVIEW" if analysis.decision == "REVIEW" else "APPROVED"

    sms_notification_obj = None
    user_explanation = ""
    user_message = ""
    now_str = datetime.now().strftime("%H:%M ngày %d/%m/%Y")

    if tx.status == "APPROVED":
        user_message = "Đặt hàng & Thanh toán thành công!"
        user_explanation = "Giao dịch đã được hệ thống AI thẩm định và phê duyệt an toàn tuyệt đối."
        sms_content = (
            f"[ECOMMERCE SECURE PAY] Cảm ơn Quý khách {user.name} ({phone_number})! "
            f"Đơn hàng #{tx.id[:8].upper()} ({items_summary}) trị giá {tx.amount:,.0f} VND "
            f"đã được thanh toán thành công lúc {now_str}. "
            f"Đơn hàng sẽ sớm được giao đến: {shipping_address}. Hotline hỗ trợ: 1900-8888."
        )
        sms_notification_obj = models.SmsNotification(
            user_id=user.id,
            phone=phone_number,
            order_id=tx.id,
            message_type="ORDER_SUCCESS",
            content=sms_content,
            status="SENT",
        )
        db.add(sms_notification_obj)

    else:
        user_message = f"Giao dịch đã bị tạm khóa để bảo vệ tài khoản ({analysis.risk_level} - {analysis.risk_score}/100 điểm)"
        friendly_reasons = format_signals_for_user(analysis.signals)
        user_explanation = (
            f"Hệ thống bảo mật AI phát hiện dấu hiệu bất thường: {friendly_reasons}. "
            f"Để đảm bảo an toàn số dư tài khoản của Quý khách, giao dịch này chưa được phê duyệt. "
            f"Vui lòng kiểm tra lại thông tin hoặc liên hệ Hotline 1900-8888 để được hỗ trợ mở khóa."
        )

        db.add(
            models.FraudAlert(
                transaction_id=tx.id,
                user_id=user.id,
                risk_score=analysis.risk_score,
                risk_level=analysis.risk_level,
                title=f"Cảnh báo gian lận: {analysis.risk_level} Risk (Điểm: {analysis.risk_score})",
                description=f"Giao dịch #{tx.id[:8].upper()} của {user.name} bị chặn do: {friendly_reasons[:120]}",
                evidence_json=json.dumps([s.model_dump(by_alias=True) for s in analysis.signals]),
                status="OPEN",
            )
        )

        sms_content = (
            f"[CẢNH BÁO AN TOÀN] Tài khoản {user.name} ({phone_number}): "
            f"Giao dịch #{tx.id[:8].upper()} trị giá {tx.amount:,.0f} VND bị TỪ CHỐI lúc {now_str} "
            f"do vi phạm chính sách an toàn AI ({friendly_reasons[:70]}...). "
            f"Nếu KHÔNG phải bạn thực hiện, vui lòng khóa thẻ hoặc đổi mật khẩu ngay!"
        )
        sms_notification_obj = models.SmsNotification(
            user_id=user.id,
            phone=phone_number,
            order_id=tx.id,
            message_type="ORDER_BLOCKED",
            content=sms_content,
            status="SENT",
        )
        db.add(sms_notification_obj)

    db.commit()

    return {
        "status": tx.status,
        "decision": analysis.decision,
        "userMessage": user_message,
        "userExplanation": user_explanation,
        "transaction": {
            "id": tx.id,
            "shortId": "#TX-" + tx.id[:8].upper(),
            "userId": tx.user_id,
            "userName": user.name,
            "userPhone": phone_number,
            "amount": tx.amount,
            "status": tx.status,
            "paymentMethod": tx.payment_method,
            "itemsSummary": tx.items_summary,
            "shippingAddress": tx.shipping_address,
            "deviceId": tx.device_id,
            "ipAddress": tx.ip_address,
            "locationCity": tx.location_city,
            "createdAt": tx.created_at.strftime("%H:%M:%S %d/%m/%Y"),
        },
        "fraudAnalysis": analysis.model_dump(by_alias=True),
        "smsNotification": {
            "id": sms_notification_obj.id if sms_notification_obj else None,
            "phone": phone_number,
            "messageType": sms_notification_obj.message_type if sms_notification_obj else "NONE",
            "content": sms_notification_obj.content if sms_notification_obj else "",
            "createdAt": now_str,
        } if sms_notification_obj else None,
    }

"""

text = text[:idx_start] + new_code + text[idx_end:]

with open("python_app/main.py", "w", encoding="utf-8") as f:
    f.write(text)

print("create_transaction_api updated successfully!")
