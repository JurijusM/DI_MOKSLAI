"""
Process Hierarchy Model - Represents the full Title 1-5 hierarchy
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base

class ProcessHierarchy(Base):
    """
    Process Hierarchy - represents the full BPC hierarchy.
    
    Levels:
    1. Title 1: E2E Process (e.g., "65 Order to cash")
    2. Title 2: Process Area (e.g., "65.05 Sales management")
    3. Title 3: Business Process (e.g., "65.05.040 Develop sales catalogs")
    4. Title 4: Scenario (e.g., "65.05.040.100 Develop catalogs in D365 SCM")
    5. Title 5: Work Items (Tasks, Configuration deliverables, etc.)
    """
    
    __tablename__ = "process_hierarchy"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Sequence ID from Excel (not unique - same ID can have multiple work item types)
    sequence_id = Column(String(50), nullable=True, index=True)  # e.g., "65.05.040.100"
    
    # Hierarchy level (1-5 for Title 1-5)
    level = Column(Integer, nullable=False, index=True)
    
    # Work item type
    work_item_type = Column(String(50), nullable=True, index=True)  # Scenario, Task, Workshop, etc.
    
    # Display name
    name = Column(String(500), nullable=False)
    
    # Description
    description = Column(Text, nullable=True)
    
    # Parent relationship (self-referential)
    parent_id = Column(Integer, ForeignKey("process_hierarchy.id"), nullable=True)
    
    # Link to ERP system (for scenarios - level 4)
    erp_system_id = Column(Integer, ForeignKey("erp_systems.id"), nullable=True)
    
    # Display order
    display_order = Column(Integer, nullable=True)
    
    # Original Excel data
    excel_row_index = Column(Integer, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    parent = relationship("ProcessHierarchy", remote_side=[id], backref="children")
    erp_system = relationship("ERPSystem")
    requirements = relationship("HierarchyRequirement", back_populates="hierarchy_item")


class HierarchyRequirement(Base):
    """
    Requirements for hierarchy items (MoSCoW prioritization at lowest level).
    """
    
    __tablename__ = "hierarchy_requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    hierarchy_item_id = Column(Integer, ForeignKey("process_hierarchy.id"), nullable=False)
    priority = Column(String(20), nullable=False)  # 'must', 'should', 'could', 'wont'
    notes = Column(Text, nullable=True)
    selected_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization")
    hierarchy_item = relationship("ProcessHierarchy", back_populates="requirements")
    selected_by_user = relationship("User")

