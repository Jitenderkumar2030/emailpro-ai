from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import enum

class DripStatus(enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"

class DripCampaign(Base):
    __tablename__ = "drip_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(DripStatus), default=DripStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="drip_campaigns")
    steps = relationship("DripStep", back_populates="campaign")
    subscribers = relationship("DripSubscriber", back_populates="campaign")

class DripStep(Base):
    __tablename__ = "drip_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("drip_campaigns.id"))
    step_number = Column(Integer, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    delay_days = Column(Integer, default=0)  # Days after previous step
    delay_hours = Column(Integer, default=0)  # Hours after previous step
    
    # Relationships
    campaign = relationship("DripCampaign", back_populates="steps")

class DripSubscriber(Base):
    __tablename__ = "drip_subscribers"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("drip_campaigns.id"))
    email = Column(String, nullable=False)
    current_step = Column(Integer, default=0)
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    last_email_sent = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    campaign = relationship("DripCampaign", back_populates="subscribers")