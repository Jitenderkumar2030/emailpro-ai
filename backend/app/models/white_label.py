from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class WhiteLabelConfig(Base):
    __tablename__ = "white_label_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_name = Column(String, nullable=False)
    logo_url = Column(String)
    primary_color = Column(String, default="#3B82F6")
    custom_domain = Column(String)
    custom_css = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="white_label_config")
