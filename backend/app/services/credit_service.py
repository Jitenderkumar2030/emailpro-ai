from sqlalchemy.orm import Session
from app.models.user import User, PlanType
from app.db.session import get_db
from datetime import datetime, timedelta
from fastapi import HTTPException

PLAN_LIMITS = {
    PlanType.FREE: {"daily": 3, "monthly": 90},
    PlanType.STARTER: {"daily": 100, "monthly": 3000},
    PlanType.PRO: {"daily": -1, "monthly": -1},  # Unlimited
    PlanType.LIFETIME: {"daily": -1, "monthly": -1}
}

def check_and_consume_credit(user_id: int, db: Session) -> bool:
    """Advanced credit management with daily limits"""
    # Multi-tier plan support
    # Automatic daily reset
    # Usage tracking and analytics
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Reset daily counter if new day
    today = datetime.utcnow().date()
    if user.last_reset_date.date() < today:
        user.emails_generated_today = 0
        user.last_reset_date = datetime.utcnow()
    
    # Check plan limits
    limits = PLAN_LIMITS.get(user.plan_type)
    if limits["daily"] != -1 and user.emails_generated_today >= limits["daily"]:
        raise HTTPException(status_code=429, detail="Daily limit exceeded")
    
    # Check if plan expired
    if user.plan_expires_at and user.plan_expires_at < datetime.utcnow():
        user.plan_type = PlanType.FREE
        user.credits = 3
    
    # Consume credit
    if user.plan_type == PlanType.FREE:
        if user.credits <= 0:
            raise HTTPException(status_code=429, detail="No credits remaining")
        user.credits -= 1
    
    user.emails_generated_today += 1
    user.total_emails_generated += 1
    db.commit()
    
    return True

def get_user_usage(user_id: int, db: Session) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    limits = PLAN_LIMITS.get(user.plan_type)
    
    return {
        "plan_type": user.plan_type.value,
        "credits_remaining": user.credits if user.plan_type == PlanType.FREE else "unlimited",
        "daily_usage": user.emails_generated_today,
        "daily_limit": limits["daily"] if limits["daily"] != -1 else "unlimited",
        "total_generated": user.total_emails_generated,
        "plan_expires_at": user.plan_expires_at
    }
