from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from app.db.base import Base
from datetime import datetime

class EmailLog(Base):
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    
    recipient_email = Column(String, nullable=False)
    subject = Column(String)
    body = Column(Text)
    
    # Tracking
    sent_at = Column(DateTime, default=datetime.utcnow)
    opened_at = Column(DateTime, nullable=True)
    clicked_at = Column(DateTime, nullable=True)
    replied_at = Column(DateTime, nullable=True)
    bounced_at = Column(DateTime, nullable=True)
    
    # Status
    is_sent = Column(Boolean, default=False)
    is_opened = Column(Boolean, default=False)
    is_clicked = Column(Boolean, default=False)
    is_replied = Column(Boolean, default=False)
    is_bounced = Column(Boolean, default=False)
    
    # Tracking identifiers
    tracking_id = Column(String, unique=True, index=True)
    unsubscribe_token = Column(String, unique=True, index=True)
