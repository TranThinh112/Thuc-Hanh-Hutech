import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
try:
    from .database import Base
except ImportError:
    from database import Base

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_uuid)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False, default="")
    password_hash = Column(String, nullable=False, default="")
    role = Column(String, default="USER")  # 'USER' | 'ADMIN'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="user")
    risk_profile = relationship("UserRiskProfile", back_populates="user", uselist=False)
    fraud_alerts = relationship("FraudAlert", back_populates="user")
    sms_notifications = relationship("SmsNotification", back_populates="user")

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    stock = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="VND")
    payment_method = Column(String, nullable=False)
    status = Column(String, default="PENDING")  # APPROVED | BLOCKED | REVIEW | PENDING
    shipping_address = Column(String, nullable=True, default="")
    items_summary = Column(String, nullable=True, default="")
    admin_action = Column(String, nullable=True, default=None)  # OVERRIDE_APPROVE | CONFIRM_BLOCK | None
    admin_action_note = Column(String, nullable=True, default="")
    ip_address = Column(String, nullable=False)
    device_id = Column(String, nullable=False)
    user_agent = Column(String, nullable=False)
    location_country = Column(String, nullable=False)
    location_city = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    feature_snapshot = relationship("TransactionFeature", back_populates="transaction", uselist=False)
    fraud_analysis = relationship("FraudAnalysis", back_populates="transaction", uselist=False)
    fraud_alerts = relationship("FraudAlert", back_populates="transaction")

class TransactionFeature(Base):
    __tablename__ = "transaction_features"

    id = Column(String, primary_key=True, default=gen_uuid)
    transaction_id = Column(String, ForeignKey("transactions.id"), unique=True, nullable=False)
    amount_ratio = Column(Float, nullable=False)
    transactions_last_1m = Column(Integer, nullable=False)
    transactions_last_5m = Column(Integer, nullable=False)
    transactions_last_15m = Column(Integer, nullable=False)
    transactions_last_1h = Column(Integer, nullable=False)
    failed_transactions_last_5m = Column(Integer, nullable=False)
    different_payment_methods_15m = Column(Integer, nullable=False)
    different_devices_15m = Column(Integer, nullable=False)
    different_ips_15m = Column(Integer, nullable=False)
    is_new_device = Column(Boolean, nullable=False)
    is_new_ip = Column(Boolean, nullable=False)
    location_changed = Column(Boolean, nullable=False)
    distance_km = Column(Float, nullable=False)
    time_diff_seconds = Column(Float, nullable=False)
    impossible_travel = Column(Boolean, nullable=False)
    account_age_hours = Column(Float, nullable=False)
    failed_payment_rate = Column(Float, nullable=False)
    feature_snapshot_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    transaction = relationship("Transaction", back_populates="feature_snapshot")

class FraudAnalysis(Base):
    __tablename__ = "fraud_analyses"

    id = Column(String, primary_key=True, default=gen_uuid)
    transaction_id = Column(String, ForeignKey("transactions.id"), unique=True, nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    decision = Column(String, nullable=False)  # APPROVE | REVIEW | BLOCK
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    transaction = relationship("Transaction", back_populates="fraud_analysis")
    rule_results = relationship("FraudRuleResult", back_populates="fraud_analysis")

class FraudRuleResult(Base):
    __tablename__ = "fraud_rule_results"

    id = Column(String, primary_key=True, default=gen_uuid)
    fraud_analysis_id = Column(String, ForeignKey("fraud_analyses.id"), nullable=False)
    rule_id = Column(String, nullable=False)
    rule_name = Column(String, nullable=False)
    triggered = Column(Boolean, nullable=False)
    score = Column(Integer, nullable=False)
    severity = Column(String, nullable=False)
    reason = Column(Text, nullable=False)
    evidence_json = Column(Text, nullable=False)

    fraud_analysis = relationship("FraudAnalysis", back_populates="rule_results")

class FraudAlert(Base):
    __tablename__ = "fraud_alerts"

    id = Column(String, primary_key=True, default=gen_uuid)
    transaction_id = Column(String, ForeignKey("transactions.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    evidence_json = Column(Text, nullable=False)
    status = Column(String, default="OPEN")  # OPEN | REVIEWED | RESOLVED_FRAUD | RESOLVED_LEGIT
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transaction = relationship("Transaction", back_populates="fraud_alerts")
    user = relationship("User", back_populates="fraud_alerts")

class SmsNotification(Base):
    __tablename__ = "sms_notifications"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    phone = Column(String, nullable=False)
    order_id = Column(String, nullable=True)
    message_type = Column(String, nullable=False)  # ORDER_SUCCESS | ORDER_BLOCKED | SECURITY_ALERT
    content = Column(Text, nullable=False)
    status = Column(String, default="SENT")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sms_notifications")

class UserRiskProfile(Base):
    __tablename__ = "user_risk_profiles"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    account_age_days = Column(Float, nullable=False, default=0.0)
    total_transactions = Column(Integer, default=0)
    avg_amount = Column(Float, default=0.0)
    failed_rate = Column(Float, default=0.0)
    known_devices_json = Column(Text, nullable=False, default="[]")
    known_ips_json = Column(Text, nullable=False, default="[]")
    known_locations_json = Column(Text, nullable=False, default="[]")
    avg_risk_score = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="risk_profile")

class DeviceProfile(Base):
    __tablename__ = "device_profiles"

    id = Column(String, primary_key=True, default=gen_uuid)
    device_id = Column(String, unique=True, nullable=False)
    user_count = Column(Integer, default=1)
    transaction_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    avg_risk_score = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class IpProfile(Base):
    __tablename__ = "ip_profiles"

    id = Column(String, primary_key=True, default=gen_uuid)
    ip_address = Column(String, unique=True, nullable=False)
    user_count = Column(Integer, default=1)
    transaction_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    country = Column(String, nullable=False)
    avg_risk_score = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FraudRuleConfig(Base):
    __tablename__ = "fraud_rule_configs"

    id = Column(String, primary_key=True, default=gen_uuid)
    rule_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    weight = Column(Integer, nullable=False)
    enabled = Column(Boolean, default=True)
    triggered_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
