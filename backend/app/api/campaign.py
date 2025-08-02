# backend/app/api/campaign.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.campaign_service import process_campaign_csv
from app.services.tracking_service import get_campaign_analytics
from app.db.session import get_db
from app.models.campaign import Campaign
from app.models.email_tracking import EmailLog
from typing import List

router = APIRouter()

@router.post("/campaign/upload")
async def upload_campaign_csv(file: UploadFile = File(...)):
    try:
        campaign_result = await process_campaign_csv(file)
        return {"status": "success", "details": campaign_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/campaigns")
async def list_campaigns(db: Session = Depends(get_db)):
    try:
        campaigns = db.query(Campaign).all()
        return {"campaigns": [
            {
                "id": c.id,
                "name": c.name,
                "sent": c.sent,
                "created_at": c.created_at,
                "user_id": c.user_id
            } for c in campaigns
        ]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/campaigns/{campaign_id}/analytics")
async def get_campaign_stats(campaign_id: int, db: Session = Depends(get_db)):
    try:
        analytics = get_campaign_analytics(campaign_id, db)
        return {"analytics": analytics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/campaigns/{campaign_id}/emails")
async def get_campaign_emails(campaign_id: int, db: Session = Depends(get_db)):
    try:
        emails = db.query(EmailLog).filter(EmailLog.campaign_id == campaign_id).all()
        return {"emails": [
            {
                "id": e.id,
                "recipient_email": e.recipient_email,
                "subject": e.subject,
                "sent_at": e.sent_at,
                "is_opened": e.is_opened,
                "is_clicked": e.is_clicked,
                "is_replied": e.is_replied,
                "opened_at": e.opened_at,
                "clicked_at": e.clicked_at
            } for e in emails
        ]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tracking/pixel/{tracking_id}")
def track_email_open(tracking_id: str):
    """1x1 pixel tracking for email opens"""
    # UUID-based tracking system
    # Real-time analytics updates
