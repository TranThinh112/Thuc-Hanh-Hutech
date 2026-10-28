import json
import hashlib
from datetime import datetime, timedelta
try:
    from .database import engine, Base, SessionLocal
    from . import models
    from .fraud.types import TransactionContext, LocationData
    from .fraud.fraud_engine import fraud_engine
except ImportError:
    from database import engine, Base, SessionLocal
    import models
    from fraud.types import TransactionContext, LocationData
    from fraud.fraud_engine import fraud_engine

def hash_password(password: str) -> str:
    return hashlib.sha256(f"ecommerce_secure_salt_{password}".encode("utf-8")).hexdigest()

def seed():
    print("Re-creating Python SQLite database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("Seeding products...")
    products = [
        models.Product(name="iPhone 16 Pro Max 256GB", price=34990000.0, category="Smartphones", description="Flagship smartphone with A18 Pro chip", image_url="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80"),
        models.Product(name="MacBook Pro 14 M3 Pro", price=49990000.0, category="Laptops", description="Powerful workstation for developers and creators", image_url="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=600&q=80"),
        models.Product(name="Sony WH-1000XM5 Headphones", price=8490000.0, category="Audio", description="Industry-leading noise cancelling wireless headphones", image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80"),
        models.Product(name="Apple Watch Ultra 2", price=21990000.0, category="Wearables", description="Rugged smartwatch built for outdoor adventure", image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80"),
        models.Product(name="Samsung Galaxy S24 Ultra", price=29990000.0, category="Smartphones", description="Galaxy AI powered flagship device", image_url="https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=600&q=80"),
        models.Product(name="Wireless Mechanical Keyboard", price=2500000.0, category="Accessories", description="RGB mechanical keyboard with hot-swappable switches", image_url="https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80"),
    ]
    db.add_all(products)
    db.commit()

    print("Seeding fraud rules...")
    default_rules = [
        models.FraudRuleConfig(rule_id="HIGH_AMOUNT", name="High Transaction Amount", description="Phát hiện số tiền đơn hàng vượt ngưỡng kiểm soát (>20M, >50M, >100M VND)", weight=25, enabled=True),
        models.FraudRuleConfig(rule_id="UNUSUAL_AMOUNT", name="Unusual Amount Spike", description="Phát hiện số tiền đột biến so với mức chi tiêu trung bình lịch sử", weight=25, enabled=True),
        models.FraudRuleConfig(rule_id="TRANSACTION_VELOCITY", name="Transaction Velocity Spike", description="Phát hiện tần suất đặt hàng dồn dập trong khoảng thời gian ngắn (5 phút)", weight=30, enabled=True),
        models.FraudRuleConfig(rule_id="FAILED_ATTEMPT_VELOCITY", name="Failed Payment Velocity", description="Phát hiện hành vi thử thẻ liên tục (Card Testing Attack)", weight=25, enabled=True),
        models.FraudRuleConfig(rule_id="NEW_DEVICE", name="New Device Detected", description="Phát hiện đăng nhập và thanh toán từ thiết bị lạ chưa từng sử dụng", weight=15, enabled=True),
        models.FraudRuleConfig(rule_id="NEW_IP", name="New IP Address Detected", description="Phát hiện địa chỉ IP truy cập mới hoàn toàn", weight=10, enabled=True),
        models.FraudRuleConfig(rule_id="LOCATION_CHANGE", name="Location Change / Impossible Travel", description="Phát hiện di chuyển bất khả thi (Impossible Travel) giữa các vị trí địa lý", weight=35, enabled=True),
        models.FraudRuleConfig(rule_id="PAYMENT_METHOD_SWITCHING", name="Rapid Payment Method Switching", description="Phát hiện chuyển đổi liên tục nhiều thẻ/phương thức thanh toán khác nhau", weight=20, enabled=True),
        models.FraudRuleConfig(rule_id="MULTIPLE_DEVICES", name="Multiple Devices Anomaly", description="Phát hiện nhiều thiết bị cùng sử dụng một tài khoản trong 15 phút", weight=25, enabled=True),
        models.FraudRuleConfig(rule_id="MULTIPLE_IPS", name="Multiple IP Addresses Anomaly", description="Phát hiện nhiều IP khác nhau thực hiện giao dịch trong thời gian ngắn", weight=20, enabled=True),
        models.FraudRuleConfig(rule_id="ACCOUNT_AGE", name="New Account Risk", description="Đánh giá rủi ro tài khoản mới tạo lập (<24h)", weight=15, enabled=True),
        models.FraudRuleConfig(rule_id="FAILED_PAYMENT_RATE", name="High Failed Payment Rate", description="Đánh giá tỷ lệ giao dịch thất bại cao bất thường của người dùng", weight=15, enabled=True),
        models.FraudRuleConfig(rule_id="SUSPICIOUS_COMPOSITE_PATTERN", name="Suspicious Composite Fraud Patterns", description="Phát hiện các mẫu hình tấn công phức hợp (Account Takeover, Card Testing)", weight=30, enabled=True),
    ]
    db.add_all(default_rules)
    db.commit()

    print("Seeding requested users...")
    thinh = models.User(
        username="thinh",
        name="Thịnh",
        phone="0972445090",
        email="thinh@gmail.com",
        password_hash=hash_password("123"),
        role="USER"
    )
    dat = models.User(
        username="dat",
        name="Đạt",
        phone="0981234567",
        email="dat@gmail.com",
        password_hash=hash_password("123"),
        role="USER"
    )
    dong = models.User(
        username="dong",
        name="Đông",
        phone="0977654321",
        email="dong@gmail.com",
        password_hash=hash_password("123"),
        role="USER"
    )
    admin = models.User(
        username="admin",
        name="Quản Trị Viên (Admin)",
        phone="0909999888",
        email="admin@ecommerce.vn",
        password_hash=hash_password("123"),
        role="ADMIN"
    )

    db.add_all([thinh, dat, dong, admin])
    db.commit()

    print("Seeding sample transactions & running Fraud Engine...")
    sample_txs = [
        # Giao dich 1: Thinh mua hop le
        {
            "user": thinh,
            "amount": 8490000.0,
            "payment_method": "VISA",
            "ip": "113.161.44.12",
            "device": "device_thinh_iphone",
            "city": "Hà Nội",
            "country": "Vietnam",
            "items": "Sony WH-1000XM5 Headphones",
            "address": "Số 15 Cầu Giấy, Hà Nội",
        },
        # Giao dich 2: Dat mua hop le
        {
            "user": dat,
            "amount": 2500000.0,
            "payment_method": "MOMO",
            "ip": "14.161.12.99",
            "device": "device_dat_laptop",
            "city": "Hồ Chí Minh",
            "country": "Vietnam",
            "items": "Wireless Mechanical Keyboard",
            "address": "Quận 1, TP. Hồ Chí Minh",
        },
        # Giao dich 3: Ke gian danh cap tai khoan Dong de mua laptop dat tien tu IP Tokyo -> BLOCKED
        {
            "user": dong,
            "amount": 49990000.0,
            "payment_method": "VISA",
            "ip": "185.220.101.5",
            "device": "device_hacker_kali",
            "city": "Tokyo",
            "country": "Japan",
            "items": "MacBook Pro 14 M3 Pro",
            "address": "Shibuya, Tokyo, Japan",
        },
        # Giao dich 4: Nghi van tan cong thu the (Card Testing) tai khoan Thinh -> BLOCKED
        {
            "user": thinh,
            "amount": 34990000.0,
            "payment_method": "VISA",
            "ip": "45.142.120.10",
            "device": "device_bot_script",
            "city": "London",
            "country": "United Kingdom",
            "items": "iPhone 16 Pro Max 256GB",
            "address": "Westminster, London",
        }
    ]

    for item in sample_txs:
        u = item["user"]
        tx = models.Transaction(
            user_id=u.id,
            amount=item["amount"],
            currency="VND",
            payment_method=item["payment_method"],
            status="PENDING",
            items_summary=item["items"],
            shipping_address=item["address"],
            ip_address=item["ip"],
            device_id=item["device"],
            user_agent="Mozilla/5.0 Client Demo",
            location_city=item["city"],
            location_country=item["country"],
            latitude=21.0285 if item["city"] == "Hà Nội" else 10.8231 if item["city"] == "Hồ Chí Minh" else 35.6762,
            longitude=105.8542 if item["city"] == "Hà Nội" else 106.6297 if item["city"] == "Hồ Chí Minh" else 139.6503,
        )
        db.add(tx)
        db.commit()

        # Build context & analyze
        ctx = TransactionContext(
            transaction_id=tx.id,
            user_id=u.id,
            amount=tx.amount,
            currency="VND",
            payment_method=tx.payment_method,
            ip_address=tx.ip_address,
            device_id=tx.device_id,
            user_agent=tx.user_agent,
            location=LocationData(country=tx.location_country, city=tx.location_city),
            timestamp=tx.created_at,
            account_age_hours=120.0,
            previous_transaction_count=3,
            previous_failed_transaction_count=0 if "hacker" not in item["device"] else 3,
            average_transaction_amount=4000000.0,
            max_previous_amount=10000000.0,
            user_known_devices=["device_thinh_iphone", "device_dat_laptop"],
            user_known_ips=["113.161.44.12", "14.161.12.99"],
            user_known_locations=["Hà Nội", "Hồ Chí Minh"],
        )
        analysis = fraud_engine.analyze_transaction(ctx)

        feat = models.TransactionFeature(
            transaction_id=tx.id,
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
        db.add(feat)

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
            rr = models.FraudRuleResult(
                fraud_analysis_id=fa.id,
                rule_id=sig.rule,
                rule_name=sig.rule,
                triggered=True,
                score=sig.score,
                severity=sig.severity,
                reason=sig.reason,
                evidence_json=json.dumps(sig.evidence),
            )
            db.add(rr)

        tx.status = "BLOCKED" if analysis.decision == "BLOCK" else "REVIEW" if analysis.decision == "REVIEW" else "APPROVED"

        # Tạo SMS notification tương ứng
        if tx.status == "APPROVED":
            sms_body = f"[ECOMMERCE SECURE PAY] Cảm ơn Quý khách {u.name} ({u.phone})! Đơn hàng #{tx.id[:8].upper()} ({item['items']}) trị giá {tx.amount:,.0f} VND đã được thanh toán thành công lúc {tx.created_at.strftime('%H:%M %d/%m/%Y')}. Giao đến: {item['address']}. Hotline CSKH: 1900-8888."
            msg = models.SmsNotification(
                user_id=u.id,
                phone=u.phone,
                order_id=tx.id,
                message_type="ORDER_SUCCESS",
                content=sms_body,
                status="SENT"
            )
            db.add(msg)
        else:
            alert = models.FraudAlert(
                transaction_id=tx.id,
                user_id=u.id,
                risk_score=analysis.risk_score,
                risk_level=analysis.risk_level,
                title=f"Cảnh báo gian lận: {analysis.risk_level} (Điểm rủi ro: {analysis.risk_score})",
                description=f"Giao dịch {tx.id[:8]} của {u.name} bị chặn do: {analysis.explanation.splitlines()[0]}",
                evidence_json=json.dumps([s.model_dump(by_alias=True) for s in analysis.signals]),
                status="OPEN",
            )
            db.add(alert)

            sms_alert_body = f"[CẢNH BÁO AN TOÀN] Tài khoản {u.name} ({u.phone}): Đơn hàng #{tx.id[:8].upper()} trị giá {tx.amount:,.0f} VND đã bị TỪ CHỐI BẢO MẬT do phát hiện bất thường: Vị trí lạ ({item['city']}) & thiết bị chưa xác thực. Nếu không phải bạn thực hiện, vui lòng khóa thẻ ngay!"
            msg = models.SmsNotification(
                user_id=u.id,
                phone=u.phone,
                order_id=tx.id,
                message_type="ORDER_BLOCKED",
                content=sms_alert_body,
                status="SENT"
            )
            db.add(msg)

        db.commit()

    print("Seed completed successfully!")

if __name__ == "__main__":
    seed()
