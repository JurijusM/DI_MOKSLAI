"""
Seed Database - Add initial data
"""

import sys
from pathlib import Path

# Add ITER directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.database import SessionLocal
from backend.app.models import Organization, User, ERPSystem, E2EProcess

def seed_erp_systems(db):
    """Seed ERP systems."""
    systems = [
        {"code": "BC", "name": "Dynamics 365 Business Central", "category": "ERP", "display_order": 1},
        {"code": "D365F", "name": "Dynamics 365 Finance", "category": "ERP", "display_order": 2},
        {"code": "D365SCM", "name": "Dynamics 365 Supply Chain Management", "category": "ERP", "display_order": 3},
        {"code": "D365COMM", "name": "Dynamics 365 Commerce", "category": "ERP", "display_order": 4},
        {"code": "CRM", "name": "Dynamics 365 Sales", "category": "CRM", "display_order": 5},
        {"code": "D365CS", "name": "Dynamics 365 Customer Service", "category": "CRM", "display_order": 6},
        {"code": "D365FS", "name": "Dynamics 365 Field Service", "category": "CRM", "display_order": 7},
        {"code": "D365PO", "name": "Dynamics 365 Project Operations", "category": "Specialized", "display_order": 8},
        {"code": "D365HR", "name": "Dynamics 365 Human Resources", "category": "Specialized", "display_order": 9},
    ]
    
    for sys_data in systems:
        existing = db.query(ERPSystem).filter(ERPSystem.code == sys_data["code"]).first()
        if not existing:
            erp_system = ERPSystem(**sys_data)
            db.add(erp_system)
    
    db.commit()
    print("[OK] ERP Systems seeded")

def seed_test_data(db):
    """Seed test organization and user."""
    # Test organization
    org = db.query(Organization).filter(Organization.name == "Test Organization").first()
    if not org:
        org = Organization(name="Test Organization", domain="test.local")
        db.add(org)
        db.commit()
        db.refresh(org)
    
    # Test user
    user = db.query(User).filter(User.email == "test@example.com").first()
    if not user:
        user = User(
            organization_id=org.id,
            email="test@example.com",
            display_name="Test User",
            role="customer"
        )
        db.add(user)
        db.commit()
    
    print(f"[OK] Test data seeded (Org ID: {org.id}, User ID: {user.id})")
    return org.id, user.id

def main():
    """Main seeding function."""
    print("=" * 60)
    print("Seeding ITER Database")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        seed_erp_systems(db)
        org_id, user_id = seed_test_data(db)
        print("\n[OK] Database seeded successfully!")
        print(f"   Test Organization ID: {org_id}")
        print(f"   Test User ID: {user_id}")
    except Exception as e:
        print(f"\n[ERROR] Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()



