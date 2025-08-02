from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.db.session import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.auth import get_current_user
import secrets
import string

router = APIRouter()

class ProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

class APIKeyResponse(BaseModel):
    api_key: str
    created_at: str

@router.get("/profile")
def get_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "plan_type": current_user.plan_type.value,
        "credits": current_user.credits,
        "gmail_connected": current_user.gmail_connected,
        "created_at": current_user.created_at,
        "api_key": current_user.api_key
    }

@router.put("/profile")
def update_profile(
    payload: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if payload.full_name:
        current_user.full_name = payload.full_name
    
    if payload.email:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == payload.email, User.id != current_user.id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = payload.email
    
    db.commit()
    return {"message": "Profile updated successfully"}

@router.post("/change-password")
def change_password(
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(payload.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    current_user.hashed_password = hash_password(payload.new_password)
    db.commit()
    return {"message": "Password changed successfully"}

@router.post("/generate-api-key")
def generate_api_key(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Generate secure API key
    api_key = "epa_" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    
    current_user.api_key = api_key
    db.commit()
    
    return {"api_key": api_key, "message": "API key generated successfully"}

@router.delete("/revoke-api-key")
def revoke_api_key(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.api_key = None
    db.commit()
    return {"message": "API key revoked successfully"}