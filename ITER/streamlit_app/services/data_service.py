"""
Data Service - Database access for Streamlit
"""

import sys
from pathlib import Path

# Add ITER directory to path
ITER_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ITER_DIR))

from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, get_db
from backend.app.models import (
    Organization, User, E2EProcess, BusinessProcess, 
    Scenario, CustomerRequirement, ERPSystem
)

class DataService:
    """Service for accessing database from Streamlit."""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
    
    # Organization methods
    def get_organization(self, org_id: int):
        """Get organization by ID."""
        return self.db.query(Organization).filter(Organization.id == org_id).first()
    
    # E2E Process methods
    def get_all_e2e_processes(self):
        """Get all end-to-end processes."""
        return self.db.query(E2EProcess).order_by(E2EProcess.display_order).all()
    
    # Business Process methods
    def get_business_processes(self, e2e_process_id: int = None):
        """Get business processes, optionally filtered by E2E process."""
        query = self.db.query(BusinessProcess)
        if e2e_process_id:
            query = query.filter(BusinessProcess.e2e_process_id == e2e_process_id)
        return query.order_by(BusinessProcess.display_order).all()
    
    def get_business_process(self, process_id: int):
        """Get a single business process by ID."""
        return self.db.query(BusinessProcess).filter(BusinessProcess.id == process_id).first()
    
    # Requirement methods
    def get_requirements(self, organization_id: int):
        """Get all requirements for an organization."""
        return self.db.query(CustomerRequirement).filter(
            CustomerRequirement.organization_id == organization_id
        ).all()
    
    def get_requirement(self, organization_id: int, process_id: int):
        """Get requirement for a specific process."""
        return self.db.query(CustomerRequirement).filter(
            CustomerRequirement.organization_id == organization_id,
            CustomerRequirement.business_process_id == process_id
        ).first()
    
    def save_requirement(self, organization_id: int, process_id: int, priority: str, user_id: int = None):
        """Save or update a requirement."""
        requirement = self.get_requirement(organization_id, process_id)
        
        if requirement:
            requirement.priority = priority
            requirement.selected_by = user_id
        else:
            requirement = CustomerRequirement(
                organization_id=organization_id,
                business_process_id=process_id,
                priority=priority,
                selected_by=user_id
            )
            self.db.add(requirement)
        
        self.db.commit()
        return requirement
    
    # ERP System methods
    def get_all_erp_systems(self):
        """Get all ERP systems."""
        return self.db.query(ERPSystem).order_by(ERPSystem.display_order).all()
    
    def get_erp_system(self, system_id: int):
        """Get ERP system by ID."""
        return self.db.query(ERPSystem).filter(ERPSystem.id == system_id).first()



