from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.db.session import get_db
from app.models.scheduled_email import ScheduledEmail
from app.models.user import User
from app.core.auth import get_current_user
from app.services.scheduler_service import schedule_email

router = APIRouter()

class ScheduleEmailRequest(BaseModel):
    to_email: str
    subject: str
    body: str
    scheduled_for: datetime

@router.post("/schedule")
def schedule_email_endpoint(
    payload: ScheduleEmailRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if payload.scheduled_for <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future")
    
    scheduled_email = ScheduledEmail(
        user_id=current_user.id,
        to_email=payload.to_email,
        subject=payload.subject,
        body=payload.body,
        scheduled_for=payload.scheduled_for
    )
    
    db.add(scheduled_email)
    db.commit()
    
    # Add to scheduler
    schedule_email(scheduled_email.id, payload.scheduled_for)
    
    return {"message": "Email scheduled successfully", "id": scheduled_email.id}

@router.get("/scheduled")
def get_scheduled_emails(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    emails = db.query(ScheduledEmail).filter(
        ScheduledEmail.user_id == current_user.id,
        ScheduledEmail.is_sent == False
    ).all()
    
    return [
        {
            "id": email.id,
            "to_email": email.to_email,
            "subject": email.subject,
            "scheduled_for": email.scheduled_for,
            "created_at": email.created_at
        }
        for email in emails
    ]

@router.delete("/scheduled/{email_id}")
def cancel_scheduled_email(
    email_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = db.query(ScheduledEmail).filter(
        ScheduledEmail.id == email_id,
        ScheduledEmail.user_id == current_user.id,
        ScheduledEmail.is_sent == False
    ).first()
    
    if not email:
        raise HTTPException(status_code=404, detail="Scheduled email not found")
    
    db.delete(email)
    db.commit()
    
    return {"message": "Scheduled email cancelled"}