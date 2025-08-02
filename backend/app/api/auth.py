# backend/app/api/auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_password
from app.services.gmail_service import get_gmail_auth_url, exchange_code_for_tokens

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login_user(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Return fake token for now, or use JWT if implemented
    return {
        "access_token": "fake-jwt-token",
        "token_type": "bearer"
    }

@router.get("/gmail/auth")
def get_gmail_auth(user_id: int):
    try:
        auth_url = get_gmail_auth_url(str(user_id))
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/gmail/callback")
def gmail_callback(code: str, state: str, db: Session = Depends(get_db)):
    try:
        tokens = exchange_code_for_tokens(code, state, db)
        return {"status": "success", "message": "Gmail connected successfully", "tokens": tokens}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gmail/status/{user_id}")
def gmail_connection_status(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "connected": user.gmail_connected,
        "expires_at": user.gmail_token_expires_at.isoformat() if user.gmail_token_expires_at else None
    }
