auth_code = """
# =========================================================================
# AUTHENTICATION API (Access Token & Refresh Token)
# =========================================================================

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
        "user": {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "phone": user.phone,
            "email": user.email,
            "role": user.role,
        }
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
            "user": {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "phone": user.phone,
                "role": user.role,
            }
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh Token da het han hoac khong dung")

@app.get("/api/auth/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "name": current_user.name,
        "phone": current_user.phone,
        "email": current_user.email,
        "role": current_user.role,
    }

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
"""

with open("python_app/main.py", "r", encoding="utf-8") as f:
    main_text = f.read()

if "/api/auth/login" not in main_text:
    target = 'def health_check():\n    return {\n        "status": "OK",\n        "service": "Payment Fraud Detection & Prevention System API (Python FastAPI)",\n        "timestamp": datetime.utcnow().isoformat(),\n    }'
    if target in main_text:
        main_text = main_text.replace(target, target + "\n" + auth_code)
    else:
        # insert after def health_check
        idx = main_text.find("def health_check():")
        end_idx = main_text.find("@app.", idx + 10)
        main_text = main_text[:end_idx] + auth_code + "\n" + main_text[end_idx:]

    with open("python_app/main.py", "w", encoding="utf-8") as f:
        f.write(main_text)
    print("Auth endpoints added to main.py successfully!")
else:
    print("Auth endpoints already present.")
