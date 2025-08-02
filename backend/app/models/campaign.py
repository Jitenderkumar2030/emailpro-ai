# backend/app/models/campaign.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.db.base import Base
from datetime import datetime

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_sent = Column(Integer, default=0)
    total_opens = Column(Integer, default=0)
    total_clicks = Column(Integer, default=0)
    total_replies = Column(Integer, default=0)
    # Advanced analytics tracking
