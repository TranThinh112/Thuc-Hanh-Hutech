import random
import ipaddress
import unicodedata
import urllib.request
import json
import os
from datetime import datetime, timedelta

from datetime import timezone

def get_vn_time():
    # Vietnam timezone GMT+7
    tz_vn = timezone(timedelta(hours=7))
    return datetime.now(tz_vn).replace(tzinfo=None)

from typing import Optional, Dict, Any, List
from fastapi import FastAPI, Depends, HTTPException, Query, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .database import get_db, Base, engine
from . import models
from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    get_current_user_optional,
    require_admin,
)
from .fraud.types import TransactionContext, LocationData, HistoricalTransaction
from .fraud.fraud_engine import fraud_engine
from .fraud.simulation_engine import run_fraud_simulation
from .fraud.evaluation_engine import run_system_evaluation

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Payment Fraud Detection & Prevention System (Python FastAPI)",
    description="Explainable, Auditability-driven Rule-Based Fraud Detection & Prevention System in Python",
    version="1.0.0",
)


_IP_GEO_CACHE: Dict[str, Dict[str, Any]] = {}

def is_public_ip(ip: str) -> bool:
    if not ip or ip in ("127.0.0.1", "localhost", "::1", "0.0.0.0", "testclient"):
        return False
    try:
        ip_obj = ipaddress.ip_address(ip)
        return not (ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved or ip_obj.is_link_local)
    except Exception:
        return False

def resolve_ip_geo(ip: str) -> Optional[Dict[str, Any]]:
    if not is_public_ip(ip):
        return None
    if ip in _IP_GEO_CACHE:
        return _IP_GEO_CACHE[ip]
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,city,lat,lon"
        req = urllib.request.Request(url, headers={"User-Agent": "FastAPI-FraudDetection/1.0"})
        with urllib.request.urlopen(req, timeout=1.2) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status") == "success":
                geo = {
                    "city": data.get("city") or "Hồ Chí Minh",
                    "country": data.get("country") or "Vietnam",
                    "lat": float(data.get("lat", 10.8231)),
                    "lng": float(data.get("lon", 106.6297)),
                }
                _IP_GEO_CACHE[ip] = geo
                return geo
    except Exception:
        pass
    return None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def build_context_from_db(transaction_id: str, db: Session) -> Optional[TransactionContext]:
    tx = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not tx:
        return None

    previous_txs = (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == tx.user_id, models.Transaction.id != tx.id)
        .order_by(models.Transaction.created_at.desc())
        .limit(20)
        .all()
    )

    prev_failed_count = sum(1 for t in previous_txs if t.status in ["FAILED", "BLOCKED"])
    sum_amounts = sum(t.amount for t in previous_txs)
    avg_amount = sum_amounts / len(previous_txs) if previous_txs else tx.amount
    max_prev_amount = max([t.amount for t in previous_txs], default=tx.amount)

    prev_tx = previous_txs[0] if previous_txs else None

    known_devices = list({t.device_id for t in previous_txs})
    known_ips = list({t.ip_address for t in previous_txs})
    known_locations = list({t.location_city for t in previous_txs})

    user = tx.user
    account_age_hours = max(0.1, (tx.created_at - user.created_at).total_seconds() / 3600.0) if user else 24.0

    recent_history = [
        HistoricalTransaction(
            timestamp=t.created_at,
            amount=t.amount,
            payment_method=t.payment_method,
            device_id=t.device_id,
            ip_address=t.ip_address,
            location=LocationData(country=t.location_country, city=t.location_city, latitude=t.latitude, longitude=t.longitude),
            status=t.status,
        )
        for t in previous_txs
    ]

    # Enhanced Context Adaptation for Scenario Presets (Deterministic Testing)
    tag = (getattr(tx, "scenario_tag", None) or "").lower()
    prev_loc = LocationData(country=prev_tx.location_country, city=prev_tx.location_city, latitude=prev_tx.latitude, longitude=prev_tx.longitude) if prev_tx else None
    prev_time = prev_tx.created_at if prev_tx else None
    prev_tx_count = len(previous_txs)

    if tag == "card_testing":
        prev_failed_count = 4
        prev_tx_count = 4
        account_age_hours = 1.0
        recent_history = [
            HistoricalTransaction(
                timestamp=tx.created_at - timedelta(seconds=(i + 1) * 25),
                amount=99_000.0,
                payment_method="MASTERCARD" if i % 2 == 0 else "VISA",
                device_id="device_bot_tester_01",
                ip_address=tx.ip_address,
                location=LocationData(country="Vietnam", city="Hồ Chí Minh", latitude=10.8231, longitude=106.6297),
                status="FAILED",
            )
            for i in range(4)
        ]
        known_devices = []
        known_ips = []
        known_locations = []
        prev_loc = LocationData(country="Vietnam", city="Hồ Chí Minh", latitude=10.8231, longitude=106.6297)
        prev_time = tx.created_at - timedelta(seconds=20)
    elif tag in ["travel", "impossible_travel"]:
        prev_loc = LocationData(country="Vietnam", city="Hà Nội", latitude=21.0285, longitude=105.8542)
        prev_time = tx.created_at - timedelta(minutes=2)
        recent_history = []
        prev_failed_count = 0
        account_age_hours = 720.0
        known_devices = ["device_windows_pc"]
        known_ips = ["113.161.44.12"]
        known_locations = ["Hà Nội"]
    elif tag in ["ato", "account_takeover"]:
        known_devices = ["device_windows_pc"]
        known_ips = ["113.161.44.12"]
        known_locations = ["Hà Nội"]
        prev_loc = LocationData(country="Vietnam", city="Hà Nội", latitude=21.0285, longitude=105.8542)
        prev_time = tx.created_at - timedelta(minutes=15)
        avg_amount = 750_000.0
        recent_history = []
        prev_failed_count = 0
        account_age_hours = 720.0
    elif tag in ["high_amount", "unusual_high_amount"]:
        avg_amount = 800_000.0
        max_prev_amount = 1_500_000.0
        known_devices = [tx.device_id, "device_windows_pc"]
        known_ips = [tx.ip_address, "113.161.44.12"]
        known_locations = [tx.location_city, "Hà Nội"]
        prev_loc = LocationData(country=tx.location_country, city=tx.location_city, latitude=tx.latitude, longitude=tx.longitude)
        prev_time = tx.created_at - timedelta(hours=12)
        recent_history = []
        prev_failed_count = 0
        account_age_hours = 720.0
        prev_tx_count = 15
    elif tag in ["velocity", "velocity_burst"]:
        known_devices = [tx.device_id, "device_windows_pc"]
        known_ips = [tx.ip_address, "113.161.44.12"]
        known_locations = [tx.location_city, "Hà Nội"]
        prev_loc = LocationData(country=tx.location_country, city=tx.location_city, latitude=tx.latitude, longitude=tx.longitude)
        prev_time = tx.created_at - timedelta(seconds=20)
        prev_failed_count = 0
        avg_amount = 2_000_000.0
        account_age_hours = 720.0
        recent_history = [
            HistoricalTransaction(
                timestamp=tx.created_at - timedelta(seconds=(i + 1) * 30),
                amount=2_000_000.0,
                payment_method="VISA" if i % 2 == 0 else "MASTERCARD",
                device_id=tx.device_id,
                ip_address=tx.ip_address,
                location=LocationData(country="Vietnam", city="Hà Nội", latitude=21.0285, longitude=105.8542),
                status="APPROVED",
            )
            for i in range(7)
        ]
    elif tag == "legit":
        known_devices = [tx.device_id, "device_windows_pc"]
        known_ips = [tx.ip_address, "113.161.44.12"]
        known_locations = [tx.location_city, "Hà Nội"]
        prev_loc = LocationData(country=tx.location_country, city=tx.location_city, latitude=tx.latitude, longitude=tx.longitude)
        prev_time = tx.created_at - timedelta(days=1)
        recent_history = []
        prev_failed_count = 0
        avg_amount = tx.amount
        account_age_hours = 720.0
    return TransactionContext(
        transaction_id=tx.id,
        user_id=tx.user_id,
        amount=tx.amount,
        currency=tx.currency,
        payment_method=tx.payment_method,
        ip_address=tx.ip_address,
        device_id=tx.device_id,
        user_agent=tx.user_agent,
        location=LocationData(
            country=tx.location_country,
            city=tx.location_city,
            latitude=tx.latitude,
            longitude=tx.longitude,
        ),
        timestamp=tx.created_at,
        account_age_hours=account_age_hours,
        previous_transaction_count=len(previous_txs),
        previous_failed_transaction_count=prev_failed_count,
        average_transaction_amount=avg_amount,
        max_previous_amount=max_prev_amount,
        previous_transaction_time=prev_time,
        previous_location=prev_loc,
        previous_device_id=prev_tx.device_id if prev_tx else None,
        previous_ip_address=prev_tx.ip_address if prev_tx else None,
        payment_method_history=list({t.payment_method for t in previous_txs}),
        recent_transactions=recent_history,
        user_known_devices=known_devices,
        user_known_ips=known_ips,
        user_known_locations=known_locations,
    )


@app.on_event("startup")
def startup_event():
    try:
        from .seed import ensure_seeded
        ensure_seeded()
    except Exception as e:
        print("Startup seed check note:", e)

@app.get("/api/client-info")
def get_client_info(request: Request):
    cf_ip = request.headers.get("cf-connecting-ip")
    fwd_ip = request.headers.get("x-forwarded-for")
    real_ip = request.headers.get("x-real-ip")
    client_host = request.client.host if request.client else "127.0.0.1"

    detected_ip = (cf_ip or (fwd_ip.split(",")[0].strip() if fwd_ip else None) or real_ip or client_host).strip()
    ua = request.headers.get("user-agent", "")
    ua_lower = ua.lower()

    if "iphone" in ua_lower or "ipad" in ua_lower:
        detected_dev = "device_apple_ios"
        dev_name = "Apple iOS (iPhone/iPad)"
    elif "android" in ua_lower:
        detected_dev = "device_android_mobile"
        dev_name = "Android Smartphone"
    elif "macintosh" in ua_lower or "mac os" in ua_lower:
        detected_dev = "device_apple_macos"
        dev_name = "Apple macOS (MacBook/iMac)"
    elif "windows" in ua_lower:
        detected_dev = "device_windows_pc"
        dev_name = "Windows PC"
    elif "linux" in ua_lower:
        detected_dev = "device_linux_pc"
        dev_name = "Linux PC"
    else:
        detected_dev = "device_web_browser"
        dev_name = "Web Browser"

    geo = resolve_ip_geo(detected_ip) if is_public_ip(detected_ip) else None
    return {
        "detectedIp": detected_ip,
        "isPublicIp": is_public_ip(detected_ip),
        "deviceId": detected_dev,
        "deviceName": dev_name,
        "city": geo["city"] if geo else "Hà Nội",
        "country": geo["country"] if geo else "Vietnam",
        "environment": "Railway / Cloud" if is_public_ip(detected_ip) else "Local / Dev"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "OK",
        "service": "Payment Fraud Detection & Prevention System API (Python FastAPI)",
        "timestamp": get_vn_time().isoformat(),
    }

# =========================================================================
# AUTHENTICATION API (Access Token & Refresh Token)
# =========================================================================

def serialize_user(user: models.User) -> Dict[str, Any]:
    now_utc = get_vn_time()
    is_locked = bool(user.locked_until and user.locked_until > now_utc)
    locked_mins = max(1, int((user.locked_until - now_utc).total_seconds() // 60) + 1) if is_locked else 0
    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "phone": user.phone,
        "email": user.email,
        "role": user.role,
        "isLocked": is_locked,
        "lockedUntil": user.locked_until.isoformat() if is_locked else None,
        "lockedMinsRemaining": locked_mins,
        "consecutiveBlocks": user.consecutive_blocks or 0,
    }

@app.post("/api/auth/register")
def register(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    username = str(payload.get("username", "")).strip().lower()
    password = str(payload.get("password", "")).strip()
    name = str(payload.get("name", "")).strip()
    phone = str(payload.get("phone", "")).strip()
    email = str(payload.get("email", "")).strip().lower()

    if not username:
        raise HTTPException(status_code=400, detail="Vui lòng nhập tên đăng nhập")
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Tên đăng nhập phải có ít nhất 3 ký tự")
    if not password:
        raise HTTPException(status_code=400, detail="Vui lòng nhập mật khẩu")
    if len(password) < 3:
        raise HTTPException(status_code=400, detail="Mật khẩu phải có ít nhất 3 ký tự")
    if not name:
        name = username.capitalize()
    if not phone:
        phone = "09" + "".join([str(abs(hash(username + str(i))) % 10) for i in range(8)])
    if not email:
        email = f"{username}@ecommerce.vn"

    if db.query(models.User).filter_by(username=username).first():
        raise HTTPException(status_code=400, detail=f"Tên đăng nhập '{username}' đã tồn tại. Vui lòng chọn tên khác.")
    if db.query(models.User).filter_by(phone=phone).first():
        raise HTTPException(status_code=400, detail=f"Số điện thoại '{phone}' đã được đăng ký.")
    if db.query(models.User).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail=f"Email '{email}' đã được đăng ký.")

    new_user = models.User(
        username=username,
        name=name,
        phone=phone,
        email=email,
        password_hash=hash_password(password),
        role="USER"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    try:
        profile = models.UserRiskProfile(
            user_id=new_user.id,
            account_age_days=0.0,
            total_transactions=0,
            avg_amount=0.0,
            failed_rate=0.0,
            known_devices_json="[]",
            known_ips_json="[]"
        )
        db.add(profile)
        db.commit()
    except Exception:
        db.rollback()

    token_data = {
        "sub": new_user.id,
        "username": new_user.username,
        "role": new_user.role,
        "name": new_user.name,
        "phone": new_user.phone,
    }
    return {
        "accessToken": create_access_token(token_data),
        "refreshToken": create_refresh_token({"sub": new_user.id, "username": new_user.username}),
        "tokenType": "bearer",
        "user": serialize_user(new_user),
        "message": f"Đăng ký tài khoản '{username}' thành công!"
    }

@app.post("/api/auth/login")
def login(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    account = str(payload.get("username", "")).strip()
    password = str(payload.get("password", "")).strip()

    if not account or not password:
        raise HTTPException(status_code=400, detail="Vui long nhap tai khoan va mat khau")

    user = db.query(models.User).filter(
        (models.User.username == account) |
        (models.User.phone == account) |
        (models.User.email == account)
    ).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Tai khoan hoac mat khau khong dung")

    token_data = {
        "sub": user.id,
        "username": user.username,
        "role": user.role,
        "name": user.name,
        "phone": user.phone,
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token({"sub": user.id, "username": user.username})

    return {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "tokenType": "bearer",
        "user": serialize_user(user)
    }

@app.post("/api/auth/refresh")
def refresh_token(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    ref_token = payload.get("refreshToken")
    if not ref_token:
        raise HTTPException(status_code=400, detail="Thieu Refresh Token")
    try:
        decoded = decode_token(ref_token)
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token khong hop le")
        user_id = decoded.get("sub")
        user = db.query(models.User).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="Nguoi dung khong ton tai")

        token_data = {
            "sub": user.id,
            "username": user.username,
            "role": user.role,
            "name": user.name,
            "phone": user.phone,
        }
        new_access = create_access_token(token_data)
        new_refresh = create_refresh_token({"sub": user.id, "username": user.username})
        return {
            "accessToken": new_access,
            "refreshToken": new_refresh,
            "tokenType": "bearer",
            "user": serialize_user(user)
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh Token da het han hoac khong dung")

@app.get("/api/auth/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    return serialize_user(current_user)

@app.get("/api/auth/profile")
def get_profile(current_user: Optional[models.User] = Depends(get_current_user_optional)):
    if not current_user:
        return {"isLoggedIn": False, "user": None}
    return {"isLoggedIn": True, "user": serialize_user(current_user)}

@app.get("/api/auth/demo-accounts")
def get_demo_accounts(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "name": u.name,
            "phone": u.phone,
            "email": u.email,
            "role": u.role,
            "isDefault": (u.username == "thinh")
        }
        for u in users
    ]

@app.get("/api/user/sms-notifications")
def get_user_notifications(
    phone: Optional[str] = Query(None),
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    query = db.query(models.SmsNotification)
    if current_user:
        query = query.filter(
            (models.SmsNotification.user_id == current_user.id) |
            (models.SmsNotification.phone == current_user.phone)
        )
    elif phone:
        query = query.filter(models.SmsNotification.phone == phone)

    sms_list = query.order_by(models.SmsNotification.created_at.desc()).limit(30).all()
    return [
        {
            "id": s.id,
            "phone": s.phone,
            "orderId": s.order_id,
            "messageType": s.message_type,
            "content": s.content,
            "status": s.status,
            "createdAt": s.created_at.strftime("%H:%M:%S %d/%m/%Y"),
        }
        for s in sms_list
    ]


@app.post("/api/fraud/analyze")
def analyze_transaction(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    tx_id = payload.get("transactionId")
    custom_context = payload.get("customContext")

    ctx = None
    if tx_id:
        ctx = build_context_from_db(tx_id, db)
    elif custom_context:
        ctx = TransactionContext(**custom_context)

    if not ctx:
        raise HTTPException(status_code=400, detail="Missing transactionId or customContext")

    rule_configs_db = db.query(models.FraudRuleConfig).all()
    custom_rule_configs = {r.rule_id: {"weight": r.weight, "enabled": r.enabled} for r in rule_configs_db}

    analysis = fraud_engine.analyze_transaction(ctx, custom_rule_configs)

    if tx_id:
        feat_obj = db.query(models.TransactionFeature).filter_by(transaction_id=tx_id).first()
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
        if feat_obj:
            for k, v in feat_data.items():
                setattr(feat_obj, k, v)
        else:
            feat_obj = models.TransactionFeature(transaction_id=tx_id, **feat_data)
            db.add(feat_obj)

        fa_obj = db.query(models.FraudAnalysis).filter_by(transaction_id=tx_id).first()
        if fa_obj:
            fa_obj.risk_score = analysis.risk_score
            fa_obj.risk_level = analysis.risk_level
            fa_obj.decision = analysis.decision
            fa_obj.explanation = analysis.explanation
        else:
            fa_obj = models.FraudAnalysis(
                transaction_id=tx_id,
                risk_score=analysis.risk_score,
                risk_level=analysis.risk_level,
                decision=analysis.decision,
                explanation=analysis.explanation,
            )
            db.add(fa_obj)
        db.commit()

        db.query(models.FraudRuleResult).filter_by(fraud_analysis_id=fa_obj.id).delete()
        for sig in analysis.signals:
            db.add(
                models.FraudRuleResult(
                    fraud_analysis_id=fa_obj.id,
                    rule_id=sig.rule,
                    rule_name=sig.rule,
                    triggered=True,
                    score=sig.score,
                    severity=sig.severity,
                    reason=sig.reason,
                    evidence_json=json.dumps(sig.evidence),
                )
            )

        tx = db.query(models.Transaction).filter_by(id=tx_id).first()
        if tx:
            tx.status = "BLOCKED" if analysis.decision == "BLOCK" else "REVIEW" if analysis.decision == "REVIEW" else "APPROVED"

        if analysis.risk_score >= 60 or analysis.decision != "APPROVE":
            db.add(
                models.FraudAlert(
                    transaction_id=tx_id,
                    user_id=ctx.user_id,
                    risk_score=analysis.risk_score,
                    risk_level=analysis.risk_level,
                    title=f"Fraud Alert: {analysis.risk_level} Risk Detected",
                    description=f"Transaction {tx_id} scored {analysis.risk_score}/100. Decision: {analysis.decision}",
                    evidence_json=json.dumps([s.model_dump(by_alias=True) for s in analysis.signals]),
                    status="OPEN",
                )
            )
        db.commit()

    res = analysis.model_dump(by_alias=True)
    res["transactionId"] = ctx.transaction_id
    res["userId"] = ctx.user_id
    return res

def clean_product_summary(raw: Optional[str], amount: float = 0.0) -> str:
    if not raw or not raw.strip():
        return "Sản phẩm công nghệ cao cấp"
    lower = raw.lower()
    if any(k in lower for k in ("attack", "attempt", "attacker", "hack")):
        if amount >= 100000000:
            return "MacBook Pro 16 M3 Max (64GB RAM / 1TB SSD) Space Black"
        elif amount >= 40000000:
            return "MacBook Pro 14 M3 Pro (18GB/512GB)"
        elif amount >= 20000000:
            return "iPhone 16 Pro Max 256GB"
        elif amount >= 5000000:
            return "Sony WH-1000XM5 Headphones"
        elif amount >= 1000000:
            return "Wireless Mechanical Keyboard"
        else:
            return "Cáp sạc Baseus 100W Type-C bọc dù siêu bền"
    return raw

def strip_accents(text: str) -> str:
    if not text:
        return ""
    clean = text.replace("đ", "d").replace("Đ", "d")
    nfkd = unicodedata.normalize("NFKD", clean)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()

@app.get("/api/fraud/transactions")
def get_transactions(
    riskLevel: Optional[str] = Query(None),
    decision: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    current_admin: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(models.Transaction)
    txs = query.order_by(models.Transaction.created_at.desc()).all()

    search_q = (search or "").strip()
    norm_q = strip_accents(search_q)

    filter_target = (status_filter or decision or "").strip().upper()

    result = []
    for t in txs:
        fa = t.fraud_analysis
        if riskLevel and (not fa or fa.risk_level != riskLevel):
            continue

        if filter_target:
            if filter_target in ("REVIEW", "CHO_DUYET"):
                if t.status != "REVIEW":
                    continue
            elif filter_target in ("BLOCK", "BLOCKED", "CHAN"):
                if t.status != "BLOCKED":
                    continue
            elif filter_target in ("APPROVE", "APPROVED", "DUYET"):
                if t.status != "APPROVED":
                    continue
            else:
                if (not fa or fa.decision != filter_target) and t.status != filter_target:
                    continue

        if search_q:
            u_name = (t.user.name or "") if t.user else ""
            u_user = (t.user.username or "") if t.user else ""
            u_phone = (t.user.phone or "") if t.user else ""
            tx_id = (t.id or "")
            short_id = ("#TX-" + tx_id[:8].upper())
            items = (t.items_summary or "")
            ip = (t.ip_address or "")
            city = (t.location_city or "")

            blob = f"{u_name} {u_user} {u_phone} {tx_id} {short_id} {items} {ip} {city}".lower()
            blob_norm = strip_accents(blob)

            if search_q.lower() not in blob and norm_q not in blob_norm:
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
            "itemsSummary": clean_product_summary(t.items_summary, t.amount),
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
            "scenarioTag": getattr(t, "scenario_tag", None),
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

@app.get("/api/fraud/transactions/{id}")
def get_transaction_detail(id: str, db: Session = Depends(get_db)):
    tx = db.query(models.Transaction).filter_by(id=id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    user_history = (
        db.query(models.Transaction)
        .filter_by(user_id=tx.user_id)
        .order_by(models.Transaction.created_at.asc())
        .limit(20)
        .all()
    )

    fa = tx.fraud_analysis
    feat = tx.feature_snapshot

    rule_results = []
    if fa:
        for r in fa.rule_results:
            rule_results.append({
                "id": r.id,
                "ruleId": r.rule_id,
                "ruleName": r.rule_name,
                "triggered": r.triggered,
                "score": r.score,
                "severity": r.severity,
                "reason": r.reason,
                "evidence": json.loads(r.evidence_json) if r.evidence_json else {},
            })

    return {
        "transaction": {
            "id": tx.id,
            "userId": tx.user_id,
            "amount": tx.amount,
            "currency": tx.currency,
            "paymentMethod": tx.payment_method,
            "status": tx.status,
            "ipAddress": tx.ip_address,
            "deviceId": tx.device_id,
            "userAgent": tx.user_agent,
            "locationCity": tx.location_city,
            "locationCountry": tx.location_country,
            "createdAt": tx.created_at.isoformat(),
            "user": {"name": tx.user.name, "email": tx.user.email} if tx.user else None,
            "featureSnapshot": {"featureSnapshotJson": feat.feature_snapshot_json} if feat else None,
            "fraudAnalysis": {
                "riskScore": fa.risk_score,
                "riskLevel": fa.risk_level,
                "decision": fa.decision,
                "explanation": fa.explanation,
                "ruleResults": rule_results,
            } if fa else None,
        },
        "timeline": [
            {
                "id": t.id,
                "amount": t.amount,
                "paymentMethod": t.payment_method,
                "deviceId": t.device_id,
                "ipAddress": t.ip_address,
                "location": f"{t.location_city}, {t.location_country}",
                "status": t.status,
                "timestamp": t.created_at.isoformat(),
            }
            for t in user_history
        ],
    }

@app.patch("/api/admin/transactions/{tx_id}/action")
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

    # BẢO MẬT: Chỉ cho phép admin duyệt/thao tác đối với đơn hàng đang ở trạng thái chờ duyệt (REVIEW).
    # Những đơn hàng đã bị hệ thống chặn (BLOCKED) thì admin cũng tuyệt đối không được phép mở lại!
    if tx.status == "BLOCKED" and action == "OVERRIDE_APPROVE":
        raise HTTPException(
            status_code=403, 
            detail="Đơn hàng đã bị hệ thống phòng chống gian lận chặn vi phạm nghiêm trọng (BLOCKED). Quản trị viên không được phép mở lại đơn này!"
        )

    tx.admin_action = action
    tx.admin_action_note = note
    user_phone = tx.user.phone if (tx.user and tx.user.phone) else None
    if not user_phone and tx.user_id:
        u_obj = db.query(models.User).filter_by(id=tx.user_id).first()
        if u_obj and u_obj.phone:
            user_phone = u_obj.phone
    if not user_phone:
        user_phone = "0981234567"

    if action == "OVERRIDE_APPROVE":
        tx.status = "APPROVED"
        alerts = db.query(models.FraudAlert).filter_by(transaction_id=tx_id).all()
        for a in alerts:
            a.status = "RESOLVED_LEGIT"
            a.description += f" [Admin đã mở khóa & duyệt lúc {get_vn_time().strftime('%H:%M %d/%m')}]"

        sms_body = (
            f"[ECOMMERCE SECURE PAY] Đơn hàng #{tx.id[:8].upper()} trị giá {tx.amount:,.0f} VND đã được "
            f"Quản trị viên thẩm định an toàn và PHÊ DUYỆT THÀNH CÔNG. Đơn hàng đang được đóng gói giao ngay! Hotline: 1900-8888."
        )
        db.add(models.SmsNotification(
            user_id=tx.user_id,
            phone=user_phone,
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
            a.description += f" [Admin đã xác nhận chặn gian lận lúc {get_vn_time().strftime('%H:%M %d/%m')}]"

        sms_body = (
            f"[SECURE-PAY] Đơn hàng #{tx.id[:8].upper()} trị giá {tx.amount:,.0f} VND đã bị "
            f"Quản trị viên TỪ CHỐI sau khi thẩm định rủi ro. Vui lòng liên hệ Hotline 1900-8888 nếu cần hỗ trợ."
        )
        db.add(models.SmsNotification(
            user_id=tx.user_id,
            phone=user_phone,
            order_id=tx.id,
            message_type="ORDER_BLOCKED",
            content=sms_body,
            status="SENT"
        ))

    db.commit()
    return {
        "message": "Thao tác thành công",
        "status": tx.status,
        "adminAction": tx.admin_action,
        "transactionId": tx.id
    }

@app.get("/api/fraud/alerts")
def get_alerts(status: Optional[str] = Query(None), current_admin: models.User = Depends(require_admin), db: Session = Depends(get_db)):
    query = db.query(models.FraudAlert)
    if status:
        query = query.filter_by(status=status)
    alerts = query.order_by(models.FraudAlert.created_at.desc()).all()

    return [
        {
            "id": a.id,
            "shortAlertId": "#ALT-" + a.id[:8].upper(),
            "transactionId": a.transaction_id,
            "shortTxId": "#TX-" + (a.transaction_id[:8].upper() if a.transaction_id else "N/A"),
            "userId": a.user_id,
            "userName": a.user.name if a.user else "Khách hàng",
            "userPhone": (a.user.phone if a.user and a.user.phone else "0972445090"),
            "riskScore": a.risk_score,
            "riskLevel": a.risk_level,
            "title": a.title,
            "description": a.description,
            "evidenceJson": a.evidence_json,
            "status": a.status,
            "createdAt": a.created_at.strftime("%H:%M %d/%m/%Y") if a.created_at else "",
            "user": {"name": a.user.name, "email": a.user.email, "phone": a.user.phone} if a.user else None,
        }
        for a in alerts
    ]

@app.patch("/api/fraud/alerts/{id}")
def update_alert_status(id: str, payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    alert = db.query(models.FraudAlert).filter_by(id=id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = payload.get("status", alert.status)
    db.commit()
    return {"id": alert.id, "status": alert.status}

@app.get("/api/fraud/rules")
def get_rules(db: Session = Depends(get_db)):
    rules = db.query(models.FraudRuleConfig).order_by(models.FraudRuleConfig.weight.desc()).all()
    return [
        {
            "id": r.id,
            "ruleId": r.rule_id,
            "name": r.name,
            "description": r.description,
            "weight": r.weight,
            "enabled": r.enabled,
            "triggeredCount": r.triggered_count,
        }
        for r in rules
    ]

@app.patch("/api/fraud/rules/{rule_id}")
def update_rule(rule_id: str, payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    rule = db.query(models.FraudRuleConfig).filter_by(rule_id=rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    if "weight" in payload:
        rule.weight = int(payload["weight"])
    if "enabled" in payload:
        rule.enabled = bool(payload["enabled"])
    db.commit()
    return {
        "id": rule.id,
        "ruleId": rule.rule_id,
        "name": rule.name,
        "description": rule.description,
        "weight": rule.weight,
        "enabled": rule.enabled,
        "triggeredCount": rule.triggered_count,
    }

@app.get("/api/fraud/statistics")
def get_statistics(current_admin: models.User = Depends(require_admin), db: Session = Depends(get_db)):
    txs = db.query(models.Transaction).all()
    total_tx = len(txs)
    blocked_tx = sum(1 for t in txs if t.status == "BLOCKED")
    review_tx = sum(1 for t in txs if t.status == "REVIEW")
    approved_tx = sum(1 for t in txs if t.status == "APPROVED")

    analyses = db.query(models.FraudAnalysis).all()
    ai_blocked = sum(1 for a in analyses if a.decision == "BLOCK")
    ai_review = sum(1 for a in analyses if a.decision == "REVIEW")
    ai_approved = sum(1 for a in analyses if a.decision == "APPROVE")

    total_score = 0
    dist = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for a in analyses:
        total_score += a.risk_score
        lvl = (a.risk_level or "LOW").upper()
        dist[lvl] = dist.get(lvl, 0) + 1

    avg_score = round(total_score / len(analyses), 1) if analyses else 0.0
    fraud_rate = round(((blocked_tx + review_tx) / total_tx) * 100, 1) if total_tx else 0.0
    open_alerts = db.query(models.FraudAlert).filter_by(status="OPEN").count()

    return {
        "totalTransactions": total_tx,
        "approvedTransactions": approved_tx,
        "reviewTransactions": review_tx,
        "blockedTransactions": blocked_tx,
        "averageRiskScore": avg_score,
        "blockRate": fraud_rate,
        "fraudRate": fraud_rate,
        "openAlerts": open_alerts,
        "riskDistribution": dist,
        "aiDecisions": {
            "approve": ai_approved,
            "review": ai_review,
            "block": ai_blocked,
        },
        "analyzed": total_tx,
        "approved": approved_tx,
        "review": review_tx,
        "blocked": blocked_tx,
        "avgRiskScore": avg_score,
    }

@app.get("/api/fraud/users/{id}/profile")
def get_user_risk_profile(id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id=id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_txs = db.query(models.Transaction).filter_by(user_id=id).order_by(models.Transaction.created_at.desc()).all()
    devices = list({t.device_id for t in user_txs})
    ips = list({t.ip_address for t in user_txs})
    locations = list({f"{t.location_city}, {t.location_country}" for t in user_txs})

    history = [
        {
            "timestamp": t.created_at.isoformat(),
            "score": t.fraud_analysis.risk_score if t.fraud_analysis else 0,
            "decision": t.fraud_analysis.decision if t.fraud_analysis else "APPROVE",
        }
        for t in user_txs
        if t.fraud_analysis
    ]

    return {
        "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role, "createdAt": user.created_at.isoformat()},
        "knownDevices": devices,
        "knownIps": ips,
        "knownLocations": locations,
        "riskHistory": history,
    }

@app.get("/api/fraud/devices")
def get_devices(db: Session = Depends(get_db)):
    txs = db.query(models.Transaction).all()
    dev_map = {}
    for t in txs:
        d_id = t.device_id
        if d_id not in dev_map:
            dev_map[d_id] = {"deviceId": d_id, "users": set(), "count": 0, "failed": 0, "scores": []}
        dev_map[d_id]["users"].add(t.user_id)
        dev_map[d_id]["count"] += 1
        if t.status in ["FAILED", "BLOCKED"]:
            dev_map[d_id]["failed"] += 1
        if t.fraud_analysis:
            dev_map[d_id]["scores"].append(t.fraud_analysis.risk_score)

    result = []
    for d_id, info in dev_map.items():
        avg_s = round(sum(info["scores"]) / len(info["scores"]), 1) if info["scores"] else 0.0
        result.append({
            "id": d_id,
            "deviceId": d_id,
            "userCount": len(info["users"]),
            "transactionCount": info["count"],
            "failedCount": info["failed"],
            "avgRiskScore": avg_s,
        })
    result.sort(key=lambda x: x["avgRiskScore"], reverse=True)
    return result

@app.get("/api/fraud/ips")
def get_ips(db: Session = Depends(get_db)):
    txs = db.query(models.Transaction).all()
    ip_map = {}
    for t in txs:
        ip_addr = t.ip_address
        if ip_addr not in ip_map:
            ip_map[ip_addr] = {"ipAddress": ip_addr, "country": t.location_country, "users": set(), "count": 0, "failed": 0, "scores": []}
        ip_map[ip_addr]["users"].add(t.user_id)
        ip_map[ip_addr]["count"] += 1
        if t.status in ["FAILED", "BLOCKED"]:
            ip_map[ip_addr]["failed"] += 1
        if t.fraud_analysis:
            ip_map[ip_addr]["scores"].append(t.fraud_analysis.risk_score)

    result = []
    for ip_addr, info in ip_map.items():
        avg_s = round(sum(info["scores"]) / len(info["scores"]), 1) if info["scores"] else 0.0
        result.append({
            "id": ip_addr,
            "ipAddress": ip_addr,
            "country": info["country"],
            "userCount": len(info["users"]),
            "transactionCount": info["count"],
            "failedCount": info["failed"],
            "avgRiskScore": avg_s,
        })
    result.sort(key=lambda x: x["avgRiskScore"], reverse=True)
    return result

@app.post("/api/fraud/simulation")
def run_simulation_api(payload: Dict[str, Any] = Body(...)):
    scenario = payload.get("scenario")
    if not scenario:
        raise HTTPException(status_code=400, detail="Missing scenario parameter")
    return run_fraud_simulation(scenario)

@app.post("/api/fraud/evaluation")
def run_evaluation_api(payload: Dict[str, Any] = Body(...)):
    sample_size = int(payload.get("sampleSize", 100))
    return run_system_evaluation(sample_size)

@app.post("/api/fraud/threshold-simulation")
def threshold_simulation_api(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    r_thresh = int(payload.get("reviewThreshold", 60))
    b_thresh = int(payload.get("blockThreshold", 80))

    analyses = db.query(models.FraudAnalysis).all()
    approved = 0
    reviewed = 0
    blocked = 0

    for a in analyses:
        if a.risk_score >= b_thresh:
            blocked += 1
        elif a.risk_score >= r_thresh:
            reviewed += 1
        else:
            approved += 1

    return {
        "reviewThreshold": r_thresh,
        "blockThreshold": b_thresh,
        "totalAnalyzed": len(analyses),
        "simulatedResults": {"approved": approved, "reviewed": reviewed, "blocked": blocked},
    }

def format_signals_for_user(signals: List[Any]) -> str:
    friendly_reasons = []
    has_high_amount = any("HIGH_AMOUNT" in (getattr(s, "rule", "") or "") for s in signals)
    has_account_age = any("ACCOUNT_AGE" in (getattr(s, "rule", "") or "") or "Account created" in (getattr(s, "reason", "") or "") for s in signals)

    for s in signals:
        rule = getattr(s, "rule", "") or ""
        reason = getattr(s, "reason", "") or ""
        if "HIGH_AMOUNT" in rule:
            if has_account_age:
                friendly_reasons.append("Vượt hạn mức ban đầu tài khoản mới (>20.000.000đ)")
            else:
                friendly_reasons.append("Đơn hàng giá trị cao (>20.000.000đ)")
        elif "ACCOUNT_AGE" in rule or "Account created" in reason:
            if not has_high_amount:
                friendly_reasons.append("Tài khoản mới tạo (<24h)")
        elif "UNUSUAL_AMOUNT" in rule:
            friendly_reasons.append("Số tiền tăng đột biến")
        elif "IMPOSSIBLE_TRAVEL" in rule or "LOCATION_CHANGE" in rule or "Impossible Travel" in reason:
            friendly_reasons.append("Vị trí đặt hàng bất thường")
        elif "NEW_DEVICE" in rule:
            friendly_reasons.append("Thiết bị lạ chưa xác thực")
        elif "NEW_IP" in rule:
            friendly_reasons.append("Địa chỉ IP mạng lạ")
        elif "TRANSACTION_VELOCITY" in rule or "VELOCITY" in rule or "Velocity" in reason:
            friendly_reasons.append("Tần suất đặt hàng quá nhanh")
        elif "CARD_TESTING" in rule or "Card Testing" in reason:
            friendly_reasons.append("Nghi vấn thử thẻ nhiều lần")
        elif "FAILED" in rule:
            friendly_reasons.append("Nhiều lần thanh toán thất bại")
        elif "ACCOUNT_TAKEOVER" in rule or "Account Takeover" in reason:
            friendly_reasons.append("Dấu hiệu tài khoản bị chiếm quyền (ATO)")
        elif "HIGH_VALUE" in rule or "High-Value" in reason:
            friendly_reasons.append("Mua giá trị lớn trên thiết bị lạ")
        else:
            friendly_reasons.append("Cảnh báo rủi ro bảo mật")
    seen = set()
    deduped = []
    for r in friendly_reasons:
        if r not in seen:
            seen.add(r)
            deduped.append(r)
    return "; ".join(deduped) if deduped else "Phát hiện rủi ro bảo mật"

@app.post("/api/transactions")
def create_transaction_api(
    request: Request,
    payload: Dict[str, Any] = Body(...),
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    amount = float(payload.get("amount", 0))
    payment_method = str(payload.get("paymentMethod", "VISA"))
    shipping_address = str(payload.get("shippingAddress", "Số 15 Cầu Giấy, Hà Nội"))
    items_summary = str(payload.get("itemsSummary", "Sản phẩm công nghệ"))
    customer_phone = str(payload.get("customerPhone", ""))
    scenario_tag = payload.get("scenarioTag") or None

    # TU DONG TRICH XUAT IP THAT TU PACKET MANG HOAC PROXY (Railway / Cloudflare / Nginx)
    forwarded_for = request.headers.get("x-forwarded-for")
    real_ip = request.headers.get("x-real-ip")
    client_host = request.client.host if request.client else "127.0.0.1"

    if forwarded_for:
        detected_real_ip = forwarded_for.split(",")[0].strip()
    elif real_ip:
        detected_real_ip = real_ip.strip()
    else:
        detected_real_ip = client_host

    # Neu nguoi dung co override bang preset kiem thu (Tokyo / London / Kali) thi uu tien
    requested_ip = payload.get("ipAddress")
    if requested_ip and requested_ip not in ["113.161.44.12", "127.0.0.1", "localhost"]:
        ip_address = str(requested_ip)
    elif detected_real_ip not in ["127.0.0.1", "localhost", "::1"]:
        ip_address = detected_real_ip
    else:
        ip_address = str(payload.get("ipAddress", "113.161.44.12"))

    # Tu dong trich xuat User-Agent & Device ID thuc te
    real_user_agent = request.headers.get("user-agent", "Mozilla/5.0 Client")
    user_agent = payload.get("userAgent") or real_user_agent

    requested_device = payload.get("deviceId")
    if requested_device and any(k in str(requested_device).lower() for k in ["hacker", "script", "foreign"]):
        device_id = requested_device
    else:
        # Tu dong gan nhan thiet bi theo trinh duyet thuc te (iPhone, Android, Windows, Mac)
        ua_lower = real_user_agent.lower()
        if "iphone" in ua_lower or "ipad" in ua_lower:
            detected_dev = "device_apple_ios"
        elif "android" in ua_lower:
            detected_dev = "device_android_mobile"
        elif "macintosh" in ua_lower:
            detected_dev = "device_apple_macos"
        else:
            detected_dev = "device_windows_pc"
        device_id = requested_device if requested_device and requested_device != "device_user_phone" else detected_dev

    city = str(payload.get("locationCity", "Hà Nội"))
    country = str(payload.get("locationCountry", "Vietnam"))

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

    # KIEM TRA KHOA TAI KHOAN DO VI PHAM 5 LAN LIEN TIEP (15 PHUT)
    now_utc = get_vn_time()
    if user and user.locked_until and user.locked_until > now_utc:
        diff_secs = (user.locked_until - now_utc).total_seconds()
        mins_left = max(1, int(diff_secs // 60) + 1)
        raise HTTPException(
            status_code=403,
            detail=f"Tài khoản {user.name} đang bị TẠM KHÓA GIAO DỊCH do vi phạm an toàn liên tiếp 5 lần. Vui lòng thử lại sau {mins_left} phút hoặc liên hệ Hotline 1900-8888 để được hỗ trợ mở khóa."
        )

    phone_number = customer_phone or (user.phone if user else "0972445090")

    # Tu dong phat hien vi tri neu nguoi dung nhap hoac chon Tokyo / London / New York
    s_addr_lower = shipping_address.lower()
    city_lower = city.lower()

    if "tokyo" in s_addr_lower or "tokyo" in city_lower or "japan" in s_addr_lower or "nhật" in s_addr_lower:
        city = "Tokyo"
        country = "Japan"
        if ip_address == "113.161.44.12":
            ip_address = "185.220.101.5"
        if device_id == "device_thinh_iphone":
            device_id = "device_hacker_kali"
    elif "london" in s_addr_lower or "london" in city_lower or "uk" in s_addr_lower or "anh" in s_addr_lower:
        city = "London"
        country = "United Kingdom"
        if ip_address == "113.161.44.12":
            ip_address = "45.142.120.10"
        if device_id == "device_thinh_iphone":
            device_id = "device_bot_script"
    elif "new york" in s_addr_lower or "new york" in city_lower or "usa" in s_addr_lower or "mỹ" in s_addr_lower:
        city = "New York"
        country = "United States"
        if ip_address == "113.161.44.12":
            ip_address = "198.51.100.25"
    elif "hồ chí minh" in s_addr_lower or "hcm" in s_addr_lower or "sài gòn" in s_addr_lower or "hồ chí minh" in city_lower:
        city = "Hồ Chí Minh"
        country = "Vietnam"

    # Tinh toan toa do chuan va nhan dien vi tri IP that neu co
    from .fraud.constants import CITY_COORDINATES
    if is_public_ip(ip_address) and (not payload.get("locationCity") or payload.get("locationCity") == "Hà Nội") and city not in ["Tokyo", "London", "New York"]:
        geo_real = resolve_ip_geo(ip_address)
        if geo_real:
            city = geo_real["city"]
            country = geo_real["country"]
            lat = geo_real["lat"]
            lng = geo_real["lng"]
            CITY_COORDINATES[city] = {"lat": lat, "lng": lng, "country": country}
    elif city in CITY_COORDINATES:
        lat = CITY_COORDINATES[city]["lat"]
        lng = CITY_COORDINATES[city]["lng"]
        country = CITY_COORDINATES[city].get("country", country)
    elif city == "Tokyo":
        lat, lng = 35.6762, 139.6503
    elif city == "London":
        lat, lng = 51.5074, -0.1278
    elif city == "New York":
        lat, lng = 40.7128, -74.0060
    elif city == "Hồ Chí Minh":
        lat, lng = 10.8231, 106.6297
    elif city == "Đà Nẵng":
        lat, lng = 16.0544, 108.2022
    else:
        city = "Hà Nội"
        country = "Vietnam"
        lat, lng = 21.0285, 105.8542

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
        latitude=lat,
        longitude=lng,
        scenario_tag=scenario_tag,
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
    now_str = get_vn_time().strftime("%H:%M ngày %d/%m/%Y")
    generated_otp = None

    if tx.status == "APPROVED":
        user.consecutive_blocks = 0
        user_message = "Đặt hàng & Thanh toán thành công!"
        user_explanation = "Giao dịch đã được hệ thống thẩm định an toàn và phê duyệt thành công."
        sms_content = (
            f"[ECOMMERCE SECURE PAY] Cảm ơn Quý khách {user.name} ({phone_number})! "
            f"Đơn hàng #{tx.id[:8].upper()} ({items_summary}) trị giá {tx.amount:,.0f} VND "
            f"đã được thanh toán thành công lúc {now_str}. "
            f"Đơn hàng sẽ sớm được giao đến: {shipping_address}. Hotline: 1900-8888."
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

    elif tx.status == "REVIEW":
        # ACTIVE USER PREVENTION: Step-Up 2FA OTP Challenge
        generated_otp = str(random.randint(100000, 999999))
        tx.otp_code = generated_otp
        tx.otp_expires_at = get_vn_time() + timedelta(minutes=5)
        tx.otp_verified = False

        user_message = "Đơn hàng đang chờ bạn xác thực bảo mật 2 lớp (Step-Up 2FA / Smart OTP)"
        user_explanation = (
            f"Hệ thống kiểm soát rủi ro phát hiện giá trị đơn hàng ({tx.amount:,.0f} VND) hoặc tần suất có dấu hiệu đột biến so với lịch sử chi tiêu. "
            f"Để bảo vệ an toàn cho số dư của bạn và phòng chống gian lận, chúng tôi đã gửi mã xác thực OTP 6 số đến số điện thoại {phone_number}. "
            f"Vui lòng nhập mã OTP để xác nhận chính chủ và mở khóa phê duyệt đơn hàng ngay lập tức!"
        )

        time_short = get_vn_time().strftime("%H:%M %d/%m")
        sms_content = (
            f"[SECURE-PAY] Ma xac thuc OTP cua ban la: {generated_otp} (Hieu luc 5 phut). "
            f"Dung de xac nhan don hang #{tx.id[:8].upper()} ({tx.amount:,.0f} VND). "
            f"TUYET DOI KHONG chia se ma nay cho bat ky ai de tranh bi chiem doat tien!"
        )
        sms_notification_obj = models.SmsNotification(
            user_id=user.id,
            phone=phone_number,
            order_id=tx.id,
            message_type="OTP_CHALLENGE",
            content=sms_content,
            status="SENT",
        )
        db.add(sms_notification_obj)

        db.add(
            models.FraudAlert(
                transaction_id=tx.id,
                user_id=user.id,
                risk_score=analysis.risk_score,
                risk_level=analysis.risk_level,
                title=f"Yêu cầu xác minh OTP: {analysis.risk_level} Risk (Điểm: {analysis.risk_score})",
                description=f"Giao dịch #{tx.id[:8].upper()} trị giá {tx.amount:,.0f} VND đang chờ người dùng nhập mã Step-Up OTP xác nhận chính chủ",
                evidence_json=json.dumps([s.model_dump(by_alias=True) for s in analysis.signals]),
                status="OPEN",
            )
        )

    else:  # BLOCKED
        user_message = f"GIAO DỊCH BỊ CHẶN ĐỨNG ĐỂ BẢO VỆ TÀI SẢN (Mức rủi ro: {analysis.risk_level} - {analysis.risk_score}/100 điểm)"
        friendly_reasons = format_signals_for_user(analysis.signals)

        user_explanation = (
            f"Hệ thống phát hiện dấu hiệu gian lận nguy hiểm cao ({friendly_reasons}). "
            f"Giao dịch này đã được TỰ ĐỘNG CHẶN ĐỨNG để ngăn chặn nguy cơ bị tẩu tán tài chính. "
            f"Nếu bạn KHÔNG thực hiện thao tác này, hãy bấm ngay nút 'Khóa Khẩn Cấp Tài Khoản' bên dưới để cô lập kẻ gian và bảo vệ số dư của bạn."
        )

        top_reasons_str = friendly_reasons.split(";")[0].strip() if friendly_reasons else "Nguy cơ gian lận cao"
        time_short = get_vn_time().strftime("%H:%M %d/%m")
        sms_content = (
            f"[CANH BAO SECURE-PAY] GD #{tx.id[:8].upper()} ({tx.amount:,.0f} VND) bi CHAN DUNG luc {time_short}. "
            f"Ly do: {top_reasons_str}. "
            f"Neu KHONG phai ban, hay KHOA KHAN CAP tai khoan hoac lien he Hotline 1900-8888 ngay!"
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

        db.add(
            models.FraudAlert(
                transaction_id=tx.id,
                user_id=user.id,
                risk_score=analysis.risk_score,
                risk_level=analysis.risk_level,
                title=f"Cảnh báo gian lận: {analysis.risk_level} Risk (Điểm: {analysis.risk_score})",
                description=f"Giao dịch #{tx.id[:8].upper()} của {user.name} bị chặn do: {user_explanation[:120]}",
                evidence_json=json.dumps([s.model_dump(by_alias=True) for s in analysis.signals]),
                status="OPEN",
            )
        )

        user.consecutive_blocks = (user.consecutive_blocks or 0) + 1
        if user.consecutive_blocks >= 5:
            LOCK_MINS = 15
            user.locked_until = get_vn_time() + timedelta(minutes=LOCK_MINS)
            lock_sms = (
                f"[CẢNH BÁO KHÓA TÀI KHOẢN] Tài khoản {user.name} ({phone_number}) đã bị TẠM KHÓA THANH TOÁN TRONG {LOCK_MINS} PHÚT "
                f"do vi phạm an toàn liên tiếp 5 lần. Vui lòng liên hệ Hotline 1900-8888 để được hỗ trợ mở khóa."
            )
            sms_notification_obj.content = lock_sms

    db.commit()

    return {
        "success": (tx.status == "APPROVED"),
        "status": tx.status,
        "decision": analysis.decision,
        "requiresOtp": (tx.status == "REVIEW"),
        "otpCode": generated_otp,
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


# =========================================================================
# ACTIVE USER PREVENTION APIS (OTP VERIFY & EMERGENCY KILL-SWITCH)
# =========================================================================

@app.post("/api/transactions/{tx_id}/verify-otp")
def verify_transaction_otp(
    tx_id: str,
    payload: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    tx = db.query(models.Transaction).filter_by(id=tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Không tìm thấy giao dịch")

    if tx.status != "REVIEW":
        return {
            "success": True,
            "message": f"Giao dịch hiện ở trạng thái {tx.status}, không cần xác thực OTP nữa.",
            "status": tx.status
        }

    input_otp = str(payload.get("otp", "")).strip()
    now = get_vn_time()

    if tx.otp_expires_at and now > tx.otp_expires_at:
        raise HTTPException(status_code=400, detail="Mã OTP đã hết hạn (quá 5 phút). Vui lòng yêu cầu gửi lại mã mới!")

    if not tx.otp_code or input_otp != tx.otp_code:
        raise HTTPException(status_code=400, detail="Mã OTP không chính xác! Vui lòng kiểm tra lại tin nhắn SMS điện thoại.")

    # OTP verified!
    tx.status = "APPROVED"
    tx.otp_verified = True

    fa = db.query(models.FraudAnalysis).filter_by(transaction_id=tx.id).first()
    if fa:
        fa.explanation += " [XÁC THỰC THÀNH CÔNG: Người dùng đã nhập đúng mã OTP chính chủ qua SMS - Hệ thống tự động chuyển sang APPROVED]."

    alerts = db.query(models.FraudAlert).filter_by(transaction_id=tx.id).all()
    for a in alerts:
        a.status = "RESOLVED_LEGIT"
        a.description += " [Khách hàng đã vượt qua thử thách Step-Up OTP 2FA an toàn]"

    user_phone = tx.user.phone if tx.user else "0972445090"
    now_str = now.strftime("%H:%M ngày %d/%m/%Y")

    success_sms = (
        f"[ECOMMERCE SECURE PAY] Xác thực OTP thành công! "
        f"Đơn hàng #{tx.id[:8].upper()} trị giá {tx.amount:,.0f} VND đã được PHÊ DUYỆT AN TOÀN lúc {now_str}. "
        f"Đơn hàng đang được đóng gói giao ngay! Hotline: 1900-8888."
    )
    sms_obj = models.SmsNotification(
        user_id=tx.user_id,
        phone=user_phone,
        order_id=tx.id,
        message_type="ORDER_SUCCESS",
        content=success_sms,
        status="SENT"
    )
    db.add(sms_obj)
    db.commit()

    return {
        "success": True,
        "message": "Xác thực mã OTP thành công! Đơn hàng đã được thẩm định an toàn và tự động PHÊ DUYỆT.",
        "status": "APPROVED",
        "transactionId": tx.id,
        "shortId": "#TX-" + tx.id[:8].upper(),
        "smsContent": success_sms
    }


@app.post("/api/user/emergency-lock")
def emergency_lock_account(
    payload: Dict[str, Any] = Body(default={}),
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    user = current_user
    if not user:
        user_id = payload.get("userId")
        phone = payload.get("phone")
        if user_id:
            user = db.query(models.User).filter_by(id=user_id).first()
        elif phone:
            user = db.query(models.User).filter_by(phone=phone).first()
    if not user:
        user = db.query(models.User).filter_by(username="thinh").first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản người dùng")

    LOCK_MINS = 30
    now = get_vn_time()
    user.locked_until = now + timedelta(minutes=LOCK_MINS)
    user.consecutive_blocks = 5

    user_phone = user.phone or "0972445090"
    now_str = now.strftime("%H:%M ngày %d/%m/%Y")
    alert_sms = (
        f"[CẢNH BÁO BẢO VỆ KHẨN CẤP] Tài khoản {user.name} ({user_phone}) đã được KÍCH HOẠT CHẾ ĐỘ ĐÓNG BĂNG THANH TOÁN KHẨN CẤP "
        f"lúc {now_str} theo yêu cầu của bạn để ngăn chặn hacker tẩu tán tiền. "
        f"Mọi giao dịch sẽ bị chặn trong {LOCK_MINS} phút. Để mở khóa sớm hoặc đổi mật khẩu, liên hệ CSKH 1900-8888."
    )
    sms_obj = models.SmsNotification(
        user_id=user.id,
        phone=user_phone,
        message_type="ACCOUNT_LOCKED",
        content=alert_sms,
        status="SENT"
    )
    db.add(sms_obj)
    db.commit()

    return {
        "success": True,
        "message": f"Đã kích hoạt CHẾ ĐỘ ĐÓNG BĂNG TÀI KHOẢN KHẨN CẤP TRONG {LOCK_MINS} PHÚT! Toàn bộ phiên đăng nhập bất thường đã bị cô lập.",
        "lockedUntil": user.locked_until.isoformat(),
        "lockedMins": LOCK_MINS,
        "smsContent": alert_sms
    }


@app.post("/api/user/emergency-unlock")
def emergency_unlock_account(
    payload: Dict[str, Any] = Body(default={}),
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    user = current_user
    if not user:
        user_id = payload.get("userId")
        phone = payload.get("phone")
        if user_id:
            user = db.query(models.User).filter_by(id=user_id).first()
        elif phone:
            user = db.query(models.User).filter_by(phone=phone).first()
    if not user:
        user = db.query(models.User).filter_by(username="thinh").first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản người dùng")

    user.locked_until = None
    user.consecutive_blocks = 0
    now_str = get_vn_time().strftime("%H:%M ngày %d/%m/%Y")
    unlock_sms = (
        f"[ECOMMERCE SECURE PAY] Tài khoản {user.name} đã được MỞ KHÓA THANH TOÁN AN TOÀN lúc {now_str}. "
        f"Bạn có thể tiếp tục mua sắm bình thường. Hotline: 1900-8888."
    )
    db.add(models.SmsNotification(
        user_id=user.id,
        phone=user.phone or "0972445090",
        message_type="ACCOUNT_UNLOCKED",
        content=unlock_sms,
        status="SENT"
    ))
    db.commit()

    return {
        "success": True,
        "message": f"Tài khoản {user.name} đã được mở khóa thành công! Bạn có thể tiếp tục giao dịch.",
    }



@app.get("/api/user/orders")
def get_user_orders(
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    if not current_user:
        return {"orders": [], "isLoggedIn": False, "totalPending": 0}

    query = db.query(models.Transaction)
    if current_user.role != "ADMIN":
        query = query.filter(models.Transaction.user_id == current_user.id)

    txs = query.order_by(models.Transaction.created_at.desc()).all()
    results = []
    now = get_vn_time()
    for tx in txs:
        fa = db.query(models.FraudAnalysis).filter_by(transaction_id=tx.id).first()
        u = tx.user or current_user
        diff_mins = (now - tx.created_at).total_seconds() / 60.0

        block_reason = ""
        if tx.status in ("BLOCKED", "REVIEW"):
            alert = db.query(models.FraudAlert).filter_by(transaction_id=tx.id).first()
            if alert and alert.description:
                desc = alert.description
                if "bị chặn do:" in desc:
                    r = desc.split("bị chặn do:", 1)[1].strip()
                    if r.startswith("Hệ thống bảo mật phát hiện dấu hiệu bất thường:"):
                        r = r.replace("Hệ thống bảo mật phát hiện dấu hiệu bất thường:", "").strip()
                    if "." in r:
                        r = r.split(".")[0].strip()
                    block_reason = r

            if not block_reason and fa:
                rule_objs = db.query(models.FraudRuleResult).filter_by(fraud_analysis_id=fa.id).all()
                crit_reasons = []
                for ro in rule_objs:
                    rid = (ro.rule_id or "").upper()
                    r_txt = (ro.reason or "").lower()
                    if "LOCATION" in rid or "TRAVEL" in rid or "impossible" in r_txt:
                        crit_reasons.append("Vị trí đặt hàng bất thường (Impossible Travel)")
                    elif "CARD_TESTING" in rid or "card testing" in r_txt:
                        crit_reasons.append("Nghi vấn thử thẻ liên tục (Card Testing)")
                    elif "VELOCITY" in rid or "velocity" in r_txt:
                        crit_reasons.append("Tần suất đặt hàng dồn dập trong thời gian ngắn")
                    elif "HIGH_AMOUNT" in rid or "20,000,000" in r_txt:
                        crit_reasons.append(f"Số tiền đơn hàng lớn ({tx.amount:,.0f}đ) vượt ngưỡng an toàn")
                    elif "UNUSUAL_AMOUNT" in rid:
                        crit_reasons.append("Số tiền tăng đột biến so với lịch sử")
                    elif "NEW_DEVICE" in rid or "device" in r_txt:
                        crit_reasons.append("Đăng nhập từ thiết bị lạ chưa xác thực")
                    elif "NEW_IP" in rid or "ip" in r_txt:
                        crit_reasons.append("Địa chỉ IP mạng mới chưa từng sử dụng")
                    elif "FAILED" in rid:
                        crit_reasons.append("Nhiều lần giao dịch thất bại liên tiếp")
                    elif "ACCOUNT_AGE" in rid:
                        crit_reasons.append("Tài khoản mới tạo chưa đủ độ tin cậy")
                if crit_reasons:
                    seen = set()
                    uniq = [x for x in crit_reasons if not (x in seen or seen.add(x))]
                    block_reason = " • ".join(uniq[:2])

            if not block_reason:
                if tx.status == "REVIEW":
                    block_reason = "Đơn hàng nằm trong ngưỡng rủi ro trung bình - cao, cần nhân viên bảo mật thẩm định thêm"
                else:
                    block_reason = "Phát hiện chỉ số rủi ro thanh toán bất thường theo chính sách an toàn thanh toán"

        if tx.status == "APPROVED":
            if diff_mins < 15:
                shipping_status = "Đang đóng gói tại kho"
                shipping_step = 2
                step_title = "Đóng gói kho"
            elif diff_mins < 90:
                shipping_status = "Đã xuất kho - Chờ shipper lấy hàng"
                shipping_step = 3
                step_title = "Chờ bàn giao"
            else:
                shipping_status = "Đang vận chuyển (Đang giao hàng)"
                shipping_step = 4
                step_title = "Đang giao hàng"
        elif tx.status == "REVIEW":
            shipping_status = "Đang giữ hàng - Chờ duyệt bảo mật"
            shipping_step = 1
            step_title = "Chờ xét duyệt"
        else:
            shipping_status = "Giao dịch bị từ chối / Tạm khóa"
            shipping_step = 0
            step_title = "Bị từ chối"

        hash_id = abs(hash(tx.id)) % 899999 + 100000
        tracking_code = f"GHN{hash_id}VN"

        results.append({
            "id": tx.id,
            "shortId": tx.id[:8].upper(),
            "amount": tx.amount,
            "currency": tx.currency or "VND",
            "status": tx.status,
            "adminAction": tx.admin_action,
            "adminActionNote": tx.admin_action_note,
            "shippingAddress": tx.shipping_address or "Số 15 Cầu Giấy, Hà Nội",
            "itemsSummary": clean_product_summary(tx.items_summary, tx.amount),
            "paymentMethod": tx.payment_method or "VISA",
            "createdAt": tx.created_at.strftime("%H:%M %d/%m/%Y"),
            "customerName": u.name if u else "Khách hàng",
            "customerPhone": u.phone if u else "0972445090",
            "shippingStatus": shipping_status,
            "shippingStep": shipping_step,
            "stepTitle": step_title,
            "trackingNumber": tracking_code,
            "carrier": "Giao Hàng Nhanh (GHN Express)",
            "estimatedDelivery": "Dự kiến 1 - 2 ngày tới",
            "riskScore": fa.risk_score if fa else 12,
            "riskLevel": fa.risk_level if fa else "LOW",
            "explanation": fa.explanation if fa else "Đã thẩm định phê duyệt an toàn.",
            "blockReason": block_reason,
            "isDeliveryPending": (tx.status == "APPROVED")
        })

    pending_count = len([o for o in results if o["isDeliveryPending"]])
    return {"orders": results, "isLoggedIn": True, "totalPending": pending_count}


@app.get("/api/store/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "category": p.category,
            "imageUrl": p.image_url,
            "stock": p.stock,
        }
        for p in products
    ]

static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
if os.path.exists(static_path):
    app.mount('/static', StaticFiles(directory=static_path), name='static')

    @app.get('/')
    def serve_index():
        return FileResponse(os.path.join(static_path, 'index.html'), headers={'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0'})

    @app.get('/{full_path:path}')
    def serve_static(full_path: str):
        target_file = os.path.join(static_path, full_path)
        if os.path.exists(target_file) and os.path.isfile(target_file):
            return FileResponse(target_file)
        return FileResponse(os.path.join(static_path, 'index.html'), headers={'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0'})


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("python_app.main:app", host="0.0.0.0", port=port, reload=False)

@app.post("/api/admin/users/{user_id}/unlock")
def unlock_user_account(
    user_id: str,
    current_admin: models.User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    u = db.query(models.User).filter_by(id=user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    u.locked_until = None
    u.consecutive_blocks = 0
    db.commit()
    return {"message": f"Đã mở khóa tài khoản {u.name} thành công", "userId": u.id, "username": u.username}
