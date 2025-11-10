"""
Hierarchy Service - Access hierarchical data
"""

import sys
from pathlib import Path

ITER_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ITER_DIR))

from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models import ProcessHierarchy, HierarchyRequirement, ERPSystem

class HierarchyService:
    """Service for accessing process hierarchy."""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
    
    def get_e2e_processes(self):
        """Get all E2E processes (Level 1)."""
        return self.db.query(ProcessHierarchy).filter(
            ProcessHierarchy.level == 1
        ).order_by(ProcessHierarchy.display_order).all()
    
    def get_children(self, parent_id: int):
        """Get children of a node."""
        return self.db.query(ProcessHierarchy).filter(
            ProcessHierarchy.parent_id == parent_id
        ).order_by(ProcessHierarchy.display_order).all()
    
    def get_hierarchy_tree(self, root_id: int = None):
        """
        Get full hierarchy tree starting from root.
        
        Args:
            root_id: If None, starts from Level 1 (E2E)
        
        Returns:
            List of dictionaries representing the tree
        """
        if root_id is None:
            # Get all E2E processes
            roots = self.get_e2e_processes()
        else:
            roots = [self.db.query(ProcessHierarchy).filter(ProcessHierarchy.id == root_id).first()]
        
        tree = []
        for root in roots:
            tree.append(self._build_tree_node(root))
        
        return tree
    
    def _build_tree_node(self, item: ProcessHierarchy) -> dict:
        """Recursively build tree node with children."""
        node = {
            'id': item.id,
            'sequence_id': item.sequence_id,
            'level': item.level,
            'name': item.name,
            'work_item_type': item.work_item_type,
            'erp_system_id': item.erp_system_id,
            'children': []
        }
        
        # Get children
        children = self.get_children(item.id)
        for child in children:
            node['children'].append(self._build_tree_node(child))
        
        return node
    
    def get_requirement(self, organization_id: int, hierarchy_item_id: int):
        """Get requirement for a hierarchy item."""
        return self.db.query(HierarchyRequirement).filter(
            HierarchyRequirement.organization_id == organization_id,
            HierarchyRequirement.hierarchy_item_id == hierarchy_item_id
        ).first()
    
    def save_requirement(self, organization_id: int, hierarchy_item_id: int, priority: str, user_id: int = None):
        """Save or update a requirement."""
        req = self.get_requirement(organization_id, hierarchy_item_id)
        
        if req:
            req.priority = priority
            req.selected_by = user_id
        else:
            req = HierarchyRequirement(
                organization_id=organization_id,
                hierarchy_item_id=hierarchy_item_id,
                priority=priority,
                selected_by=user_id
            )
            self.db.add(req)
        
        self.db.commit()
        return req
    
    def get_all_requirements(self, organization_id: int):
        """Get all requirements for an organization."""
        return self.db.query(HierarchyRequirement).filter(
            HierarchyRequirement.organization_id == organization_id
        ).all()
















