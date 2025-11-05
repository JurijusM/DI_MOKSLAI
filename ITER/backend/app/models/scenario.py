"""
Scenario Model - System-specific implementations
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class Scenario(Base):
    """Scenario model - maps business processes to ERP systems."""
    
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    scenario_code = Column(String(50), nullable=False)  # "65.05.040.100"
    business_process_id = Column(Integer, ForeignKey("business_processes.id"), nullable=False)
    erp_system_id = Column(Integer, ForeignKey("erp_systems.id"), nullable=False)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    sequence_number = Column(Integer, nullable=True)  # 100, 101, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint: one scenario code per ERP system
    __table_args__ = (
        UniqueConstraint('scenario_code', 'erp_system_id', name='uq_scenario_erp'),
    )
    
    # Relationships
    business_process = relationship("BusinessProcess", back_populates="scenarios")
    erp_system = relationship("ERPSystem", back_populates="scenarios")



