from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.models.user import User
from app.core.auth import get_current_user
from app.services.push_notification_service import send_push_notification

router = APIRouter()

class FCMTokenRequest(BaseModel):
    fcm_token: str

class QuickEmailRequest(BaseModel):
    to_email: str
    purpose: str
    tone: str = "Professional"

@router.post("/register-fcm-token")
def register_fcm_token(
    payload: FCMTokenRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.fcm_token = payload.fcm_token
    db.commit()
    return {"message": "FCM token registered successfully"}

@router.get("/dashboard-stats")
def get_mobile_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Optimized stats for mobile
    return {
        "credits_remaining": current_user.credits,
        "emails_today": current_user.emails_generated_today,
        "plan_type": current_user.plan_type.value,
        "gmail_connected": current_user.gmail_connected,
        "outlook_connected": getattr(current_user, 'outlook_connected', False)
    }

@router.post("/quick-email")
def generate_quick_email(
    payload: QuickEmailRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.services.openai_service import generate_email
    from app.services.credit_service import check_and_consume_credit
    
    # Check credits
    if not check_and_consume_credit(current_user.id, db):
        raise HTTPException(status_code=402, detail="Insufficient credits")
    
    # Generate email
    email = generate_email(payload.purpose, payload.tone, "")
    
    return {
        "email": email,
        "credits_remaining": current_user.credits - 1
    }