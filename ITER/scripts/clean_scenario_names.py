"""
Clean Scenario Names - Remove system-specific names from display
"""

import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.database import SessionLocal
from backend.app.models import ProcessHierarchy

# System names to remove
SYSTEM_NAMES = [
    "in Dynamics 365 Supply Chain Management",
    "in Dynamics 365 Business Central",
    "in Dynamics 365 Finance",
    "in Dynamics 365 Commerce",
    "in Dynamics 365 Sales",
    "in Dynamics 365 Customer Service",
    "in Dynamics 365 Field Service",
    "in Dynamics 365 Project Operations",
    "in Dynamics 365 Human Resources",
    "in Dynamics 65 Commerce",  # Typo in data
    "in Supply Chain Management",
    "in Business Central",
    "in Finance and Operations",
]

def clean_name(name: str) -> str:
    """Remove system-specific parts from name."""
    clean = name
    
    # Remove system names
    for system_name in SYSTEM_NAMES:
        clean = clean.replace(system_name, "").strip()
    
    # Remove sequence code prefix (e.g., "40.20.040.100 ")
    clean = re.sub(r'^\d+\.\d+\.\d+\.\d+\s+', '', clean)
    
    # Clean up extra spaces
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    return clean

def main():
    """Clean all scenario and work item names."""
    print("=" * 60)
    print("Cleaning Process Names")
    print("=" * 60)
    
    db = SessionLocal()
    updated = 0
    
    try:
        # Get all scenarios and work items that need cleaning
        items = db.query(ProcessHierarchy).filter(
            ProcessHierarchy.level >= 3  # Process level and below
        ).all()
        
        for item in items:
            original_name = item.name
            clean = clean_name(original_name)
            
            if clean != original_name and clean:
                item.name = clean
                updated += 1
                
                if updated <= 10:  # Show first 10 examples
                    print(f"\n  Before: {original_name}")
                    print(f"  After:  {clean}")
                
                if updated % 100 == 0:
                    print(f"  Cleaned {updated} names...")
        
        db.commit()
        print(f"\n[OK] Cleaned {updated} process names")
        
        # Show examples
        print("\nExamples of cleaned names:")
        examples = db.query(ProcessHierarchy).filter(
            ProcessHierarchy.sequence_id.in_(['40.20.040.100', '40.20.040.101', '65.05.040.100', '65.05.040.101'])
        ).all()
        
        for ex in examples:
            print(f"  {ex.sequence_id}: {ex.name}")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()










