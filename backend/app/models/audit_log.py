from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, etc.
    resource_type = Column(String, nullable=False)  # USER, CAMPAIGN, EMAIL, etc.
    resource_id = Column(String)
    details = Column(JSON)  # Additional context
    ip_address = Column(String)
    user_agent = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)

class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)  # OWNER, ADMIN, MEMBER, VIEWER
    permission_id = Column(Integer, ForeignKey("permissions.id"))
    
    # Relationships
    permission = relationship("Permission")