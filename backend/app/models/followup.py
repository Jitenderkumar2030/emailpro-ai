# backend/app/models/followup.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.db.base import Base
from datetime import datetime

class FollowUp(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    contact_email = Column(String)
    followup_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
