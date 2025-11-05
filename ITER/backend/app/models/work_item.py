"""
Work Item Model - Lowest level items (Tasks, Configuration deliverables, etc.)
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class WorkItem(Base):
    """
    Work Item model - lowest level items in the hierarchy.
    Types: Scenario, Configuration deliverable, Task, Workshop, Document deliverable
    """
    
    __tablename__ = "work_items"
    
    id = Column(Integer, primary_key=True, index=True)
    sequence_id = Column(String(50), unique=True, nullable=True)  # Full sequence like "65.05.040.100"
    work_item_type = Column(String(50), nullable=False)  # Scenario, Task, Configuration deliverable, etc.
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    
    # Hierarchical relationships
    parent_id = Column(Integer, ForeignKey("work_items.id"), nullable=True)
    level = Column(Integer, nullable=False)  # 1=E2E, 2=Area, 3=Process, 4=Scenario, 5=Work Item
    
    # Link to business process (for easier querying)
    business_process_id = Column(Integer, ForeignKey("business_processes.id"), nullable=True)
    
    # Link to ERP system (for scenarios)
    erp_system_id = Column(Integer, ForeignKey("erp_systems.id"), nullable=True)
    
    # Display order
    display_order = Column(Integer, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    parent = relationship("WorkItem", remote_side=[id], backref="children")
    business_process = relationship("BusinessProcess")
    erp_system = relationship("ERPSystem")
    requirements = relationship("WorkItemRequirement", back_populates="work_item")


class WorkItemRequirement(Base):
    """
    Customer requirements for work items (MoSCoW prioritization).
    """
    
    __tablename__ = "work_item_requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    work_item_id = Column(Integer, ForeignKey("work_items.id"), nullable=False)
    priority = Column(String(20), nullable=False)  # 'must', 'should', 'could', 'wont'
    notes = Column(Text, nullable=True)
    selected_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization")
    work_item = relationship("WorkItem", back_populates="requirements")
    selected_by_user = relationship("User")











