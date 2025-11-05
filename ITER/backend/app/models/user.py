"""
User Model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class User(Base):
    """User model for authentication and tracking."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    display_name = Column(String(255), nullable=True)
    role = Column(String(50), default="user")  # 'admin', 'consultant', 'customer'
    auth_provider = Column(String(50), nullable=True)  # 'azure_ad', 'local', 'oauth'
    external_id = Column(String(255), nullable=True)  # ID from auth provider
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    requirements = relationship("CustomerRequirement", back_populates="selected_by_user")



