"""
ERP System / Product Model
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class ERPSystem(Base):
    """Microsoft ERP System / Product model."""
    
    __tablename__ = "erp_systems"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)  # 'BC', 'D365F', 'CRM', etc.
    name = Column(String(255), nullable=False)  # 'Business Central', 'D365 Finance'
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)  # 'ERP', 'CRM', 'Specialized'
    display_order = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    scenarios = relationship("Scenario", back_populates="erp_system")



