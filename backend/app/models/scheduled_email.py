from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class ScheduledEmail(Base):
    __tablename__ = "scheduled_emails"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    to_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    scheduled_for = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="scheduled_emails")
    # Email scheduling system
