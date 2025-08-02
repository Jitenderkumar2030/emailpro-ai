import uuid
from sqlalchemy.orm import Session
from app.models.email_tracking import EmailLog
from app.models.campaign import Campaign
from datetime import datetime
from typing import Dict, List

def create_tracking_record(
    user_id: int, 
    recipient_email: str, 
    subject: str, 
    body: str,
    campaign_id: int = None,
    db: Session = None
) -> str:
    tracking_id = str(uuid.uuid4())
    unsubscribe_token = str(uuid.uuid4())
    
    email_log = EmailLog(
        user_id=user_id,
        campaign_id=campaign_id,
        recipient_email=recipient_email,
        subject=subject,
        body=body,
        tracking_id=tracking_id,
        unsubscribe_token=unsubscribe_token,
        is_sent=True
    )
    
    db.add(email_log)
    db.commit()
    
    return tracking_id

def track_email_open(tracking_id: str, db: Session):
    email_log = db.query(EmailLog).filter(EmailLog.tracking_id == tracking_id).first()
    if email_log and not email_log.is_opened:
        email_log.is_opened = True
        email_log.opened_at = datetime.utcnow()
        db.commit()

def track_email_click(tracking_id: str, db: Session):
    email_log = db.query(EmailLog).filter(EmailLog.tracking_id == tracking_id).first()
    if email_log and not email_log.is_clicked:
        email_log.is_clicked = True
        email_log.clicked_at = datetime.utcnow()
        db.commit()

def get_campaign_analytics(campaign_id: int, db: Session) -> Dict:
    logs = db.query(EmailLog).filter(EmailLog.campaign_id == campaign_id).all()
    
    total_sent = len(logs)
    total_opened = sum(1 for log in logs if log.is_opened)
    total_clicked = sum(1 for log in logs if log.is_clicked)
    total_replied = sum(1 for log in logs if log.is_replied)
    total_bounced = sum(1 for log in logs if log.is_bounced)
    
    return {
        "total_sent": total_sent,
        "total_opened": total_opened,
        "total_clicked": total_clicked,
        "total_replied": total_replied,
        "total_bounced": total_bounced,
        "open_rate": (total_opened / total_sent * 100) if total_sent > 0 else 0,
        "click_rate": (total_clicked / total_sent * 100) if total_sent > 0 else 0,
        "reply_rate": (total_replied / total_sent * 100) if total_sent > 0 else 0,
        "bounce_rate": (total_bounced / total_sent * 100) if total_sent > 0 else 0
    }