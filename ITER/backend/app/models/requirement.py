"""
Requirement Models - Customer Requirements
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class CustomerRequirement(Base):
    """Customer requirement - organization's priority for a business process."""
    
    __tablename__ = "customer_requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    business_process_id = Column(Integer, ForeignKey("business_processes.id"), nullable=False)
    priority = Column(String(20), nullable=False)  # 'must', 'should', 'optional', 'not_needed'
    notes = Column(Text, nullable=True)
    selected_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Unique constraint: one requirement per process per organization
    __table_args__ = (
        UniqueConstraint('organization_id', 'business_process_id', name='uq_org_process'),
    )
    
    # Relationships
    organization = relationship("Organization", back_populates="requirements")
    business_process = relationship("BusinessProcess", back_populates="requirements")
    selected_by_user = relationship("User", back_populates="requirements")


class RequirementHistory(Base):
    """Audit trail for requirement changes."""
    
    __tablename__ = "requirement_history"
    
    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("customer_requirements.id"), nullable=False)
    previous_priority = Column(String(20), nullable=True)
    new_priority = Column(String(20), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    change_reason = Column(Text, nullable=True)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())



