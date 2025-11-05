"""
Import Full BPC Hierarchy
Imports the complete Title 1-5 hierarchy with work items
"""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.database import SessionLocal
from backend.app.models import ProcessHierarchy, ERPSystem

# Product mapping
PRODUCT_MAPPING = {
    "Business Central": "BC",
    "Supply Chain Management": "D365SCM",
    "Finance": "D365F",
    "Finance and Operations": "D365F",
    "Commerce": "D365COMM",
    "Sales": "CRM",
    "Customer Service": "D365CS",
    "Field Service": "D365FS",
    "Project Operations": "D365PO",
    "Human Resources": "D365HR",
    "Customer Engagement": "CRM",
}

def get_erp_code_from_product(product_str):
    """Map product name to ERP code."""
    if pd.isna(product_str):
        return None
    
    product_str = str(product_str).strip()
    
    for key, code in PRODUCT_MAPPING.items():
        if key.lower() in product_str.lower():
            return code
    
    return None

def get_hierarchy_level(row):
    """Determine hierarchy level based on which Title is filled."""
    if pd.notna(row.get('Title 1')):
        return 1, row['Title 1']
    elif pd.notna(row.get('Title 2')):
        return 2, row['Title 2']
    elif pd.notna(row.get('Title 3')):
        return 3, row['Title 3']
    elif pd.notna(row.get('Title 4')):
        return 4, row['Title 4']
    elif pd.notna(row.get('Title 5')):
        return 5, row['Title 5']
    return None, None

def import_hierarchy(file_path: Path, db):
    """Import the full hierarchy from BPC catalog."""
    print(f"\nReading: {file_path.name}")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Total rows: {len(df)}")
        
        # Track parent at each level
        parent_stack = {1: None, 2: None, 3: None, 4: None, 5: None}
        
        imported = 0
        skipped = 0
        
        for idx, row in df.iterrows():
            # Get hierarchy level and name
            level, name = get_hierarchy_level(row)
            
            if not level or not name:
                skipped += 1
                continue
            
            name = str(name).strip()
            if not name:
                skipped += 1
                continue
            
            # Get sequence ID
            sequence_id = row.get('Process Sequence ID')
            if pd.notna(sequence_id):
                sequence_id = str(sequence_id).strip()
            else:
                sequence_id = None
            
            # Get work item type
            work_item_type = row.get('Work Item Type')
            if pd.notna(work_item_type):
                work_item_type = str(work_item_type).strip()
            else:
                work_item_type = None
            
            # Get product/ERP system (for scenarios)
            erp_code = None
            erp_system_id = None
            if pd.notna(row.get('Products')):
                erp_code = get_erp_code_from_product(row['Products'])
                if erp_code:
                    erp_system = db.query(ERPSystem).filter(ERPSystem.code == erp_code).first()
                    if erp_system:
                        erp_system_id = erp_system.id
            
            # Get parent ID from previous level
            parent_id = parent_stack.get(level - 1) if level > 1 else None
            
            # Check if item already exists (same sequence_id, level, and work_item_type)
            existing = None
            if sequence_id and work_item_type:
                existing = db.query(ProcessHierarchy).filter(
                    ProcessHierarchy.sequence_id == sequence_id,
                    ProcessHierarchy.level == level,
                    ProcessHierarchy.work_item_type == work_item_type
                ).first()
            elif sequence_id:
                existing = db.query(ProcessHierarchy).filter(
                    ProcessHierarchy.sequence_id == sequence_id,
                    ProcessHierarchy.level == level
                ).first()
            
            if not existing:
                # Create new hierarchy item
                item = ProcessHierarchy(
                    sequence_id=sequence_id,
                    level=level,
                    work_item_type=work_item_type,
                    name=name,
                    description=str(row.get('Description', ''))[:500] if pd.notna(row.get('Description')) else None,
                    parent_id=parent_id,
                    erp_system_id=erp_system_id,
                    display_order=idx,
                    excel_row_index=idx
                )
                db.add(item)
                db.flush()  # Get ID
                db.refresh(item)
                
                # Update parent stack for this level
                parent_stack[level] = item.id
                
                # Clear lower levels
                for lower_level in range(level + 1, 6):
                    parent_stack[lower_level] = None
                
                imported += 1
                
                if imported % 500 == 0:
                    db.commit()
                    print(f"  Imported {imported} items...")
            else:
                # Update parent stack with existing item
                parent_stack[level] = existing.id
                for lower_level in range(level + 1, 6):
                    parent_stack[lower_level] = None
        
        db.commit()
        print(f"\n[OK] Import complete:")
        print(f"  Items imported: {imported}")
        print(f"  Items skipped: {skipped}")
        
        return imported
        
    except Exception as e:
        print(f"[ERROR] Error importing: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return 0

def main():
    """Main import function."""
    print("=" * 60)
    print("ITER - Import Process Hierarchy")
    print("=" * 60)
    
    catalog_file = Path(r"C:\DI_MOKSLAI\GO_FAST\Microsoft Business Process Catalog Full August 2025.xlsx")
    
    if not catalog_file.exists():
        print(f"[ERROR] File not found: {catalog_file}")
        return
    
    db = SessionLocal()
    
    try:
        import_hierarchy(catalog_file, db)
        
        # Print summary by level
        print("\n" + "=" * 60)
        print("Hierarchy Summary:")
        print("=" * 60)
        
        for level in range(1, 6):
            count = db.query(ProcessHierarchy).filter(ProcessHierarchy.level == level).count()
            level_names = ["", "E2E (Title 1)", "Area (Title 2)", "Process (Title 3)", "Scenario (Title 4)", "Work Item (Title 5)"]
            print(f"Level {level} - {level_names[level]}: {count}")
        
        # Work item type distribution
        print("\nWork Item Types:")
        work_items = db.query(ProcessHierarchy.work_item_type, func.count(ProcessHierarchy.id)).\
            group_by(ProcessHierarchy.work_item_type).\
            order_by(func.count(ProcessHierarchy.id).desc()).all()
        
        for wit, count in work_items[:10]:
            if wit:
                print(f"  {wit}: {count}")
        
    except Exception as e:
        print(f"\n[ERROR] Import failed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    from sqlalchemy.sql import func
    main()

