"""
Update Process Names - Fix process names from Excel file
"""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.database import SessionLocal
from backend.app.models import BusinessProcess

def main():
    """Update process names from Excel."""
    print("=" * 60)
    print("Updating Process Names")
    print("=" * 60)
    
    # Read Excel
    catalog_file = Path(r"C:\DI_MOKSLAI\GO_FAST\Microsoft Business Process Catalog Full August 2025.xlsx")
    df = pd.read_excel(catalog_file)
    
    db = SessionLocal()
    updated = 0
    
    try:
        # Get all business processes
        processes = db.query(BusinessProcess).all()
        
        for bp in processes:
            # Find matching row in Excel
            matching_row = df[df['Process Sequence ID'] == f"{bp.process_code}.000"]
            
            if not matching_row.empty:
                row = matching_row.iloc[0]
                
                # Get name from Title 3
                if pd.notna(row.get('Title 3')):
                    full_name = str(row['Title 3']).strip()
                    
                    # Remove process code prefix
                    # "65.05.040 Develop sales catalogs" -> "Develop sales catalogs"
                    if bp.process_code in full_name:
                        process_name = full_name.replace(bp.process_code, "").strip()
                    else:
                        process_name = full_name
                    
                    # Update if different
                    if process_name and process_name != bp.name:
                        bp.name = process_name
                        updated += 1
                        
                        if updated % 100 == 0:
                            print(f"  Updated {updated} processes...")
        
        db.commit()
        print(f"\n[OK] Updated {updated} process names")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

