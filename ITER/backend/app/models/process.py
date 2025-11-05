"""
Process Models - E2E Processes and Business Processes
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class E2EProcess(Base):
    """End-to-End Process model (e.g., Order to Cash, Source to Pay)."""
    
    __tablename__ = "e2e_processes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)  # e.g., "order-to-cash"
    name = Column(String(255), nullable=False)  # e.g., "Order to Cash"
    description = Column(Text, nullable=True)
    display_order = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    business_processes = relationship("BusinessProcess", back_populates="e2e_process")


class BusinessProcess(Base):
    """Business Process model (e.g., "65.05.040 Develop sales catalogs")."""
    
    __tablename__ = "business_processes"
    
    id = Column(Integer, primary_key=True, index=True)
    process_code = Column(String(50), unique=True, nullable=False)  # "65.05.040"
    name = Column(String(255), nullable=False)  # "Develop sales catalogs"
    description = Column(Text, nullable=True)
    e2e_process_id = Column(Integer, ForeignKey("e2e_processes.id"), nullable=False)
    display_order = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    e2e_process = relationship("E2EProcess", back_populates="business_processes")
    scenarios = relationship("Scenario", back_populates="business_process")
    requirements = relationship("CustomerRequirement", back_populates="business_process")



