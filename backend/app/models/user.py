# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from datetime import datetime
import enum

class PlanType(enum.Enum):
    FREE = "free"
    STARTER = "starter" 
    PRO = "pro"
    LIFETIME = "lifetime"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Plan & Credits
    plan_type = Column(Enum(PlanType), default=PlanType.FREE)
    credits = Column(Integer, default=3)
    
    # OAuth Integrations
    gmail_connected = Column(Boolean, default=False)
    outlook_connected = Column(Boolean, default=False)
    
    # Enterprise Features
    api_key = Column(String, nullable=True, unique=True)
    fcm_token = Column(String, nullable=True)  # For push notifications
    outlook_access_token = Column(String, nullable=True)
    outlook_refresh_token = Column(String, nullable=True)
    outlook_token_expires_at = Column(DateTime, nullable=True)
    slack_webhook_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    owned_teams = relationship("Team", back_populates="owner")
    team_memberships = relationship("TeamMember", back_populates="user")
    scheduled_emails = relationship("ScheduledEmail", back_populates="user")
    drip_campaigns = relationship("DripCampaign", back_populates="user")
    white_label_config = relationship("WhiteLabelConfig", back_populates="user", uselist=False)
    audit_logs = relationship("AuditLog", back_populates="user")
