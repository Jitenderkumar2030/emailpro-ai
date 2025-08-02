# backend/app/models/email.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from app.db.base import Base
from datetime import datetime

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String)
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
