with open("python_app/main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: scenario_tag
old_code_1 = """    # Tao Transaction record
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
        latitude=lat,
        longitude=lng,
    )"""

new_code_1 = """    # Tao Transaction record
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
        latitude=lat,
        longitude=lng,
        scenario_tag=scenario_tag,
    )"""

if old_code_1 in content:
    content = content.replace(old_code_1, new_code_1, 1)
    print("Patched scenario_tag successfully.")
else:
    print("Warning: old_code_1 not found, checking if already patched...")

# Fix 2: history bug
old_code_2 = """        # Kịch bản tài khoản mới mua đơn hàng giá trị cao (>20 triệu)
        has_new_account_signal = (
            any("ACCOUNT_AGE" in (getattr(s, "rule", "") or "") or "Account created" in (getattr(s, "reason", "") or "") for s in analysis.signals)
            or analysis.extracted_features.account_age_hours < 48
            or len(history) == 0
        )"""

new_code_2 = """        # Kịch bản tài khoản mới mua đơn hàng giá trị cao (>20 triệu)
        past_tx_count = db.query(models.Transaction).filter(
            models.Transaction.user_id == user.id,
            models.Transaction.id != tx.id
        ).count()

        has_new_account_signal = (
            any("ACCOUNT_AGE" in (getattr(s, "rule", "") or "") or "Account created" in (getattr(s, "reason", "") or "") for s in analysis.signals)
            or analysis.extracted_features.account_age_hours < 48
            or past_tx_count == 0
        )"""

if old_code_2 in content:
    content = content.replace(old_code_2, new_code_2, 1)
    print("Patched history bug successfully.")
else:
    print("Warning: old_code_2 not found!")

with open("python_app/main.py", "w", encoding="utf-8") as f:
    f.write(content)
