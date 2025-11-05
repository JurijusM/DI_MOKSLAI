"""
Import BPC Data from Full Catalog
Imports all data from Microsoft Business Process Catalog Full August 2025.xlsx
"""

import sys
from pathlib import Path
import pandas as pd
import re

# Add ITER directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.database import SessionLocal
from backend.app.models import E2EProcess, BusinessProcess, Scenario, ERPSystem

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

def parse_process_sequence(seq_id):
    """Parse process sequence ID."""
    if pd.isna(seq_id):
        return None, None, None
    
    seq_str = str(seq_id).strip()
    parts = seq_str.split(".")
    
    if len(parts) == 4:
        # XX.XX.XXX.XXX format
        process_code = ".".join(parts[:3])  # XX.XX.XXX
        sequence_num = int(parts[3]) if parts[3].isdigit() else None
        return process_code, sequence_num, seq_str
    
    return None, None, None

def get_erp_code_from_product(product_str):
    """Map product name to ERP code."""
    if pd.isna(product_str):
        return None
    
    product_str = str(product_str).strip()
    
    for key, code in PRODUCT_MAPPING.items():
        if key.lower() in product_str.lower():
            return code
    
    return None

def import_full_catalog(file_path: Path, db):
    """Import data from the full BPC catalog."""
    print(f"\nReading: {file_path.name}")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Total rows: {len(df)}")
        
        # Track current E2E process
        current_e2e = None
        current_e2e_obj = None
        
        processes_imported = 0
        scenarios_imported = 0
        e2e_imported = 0
        
        for idx, row in df.iterrows():
            # Check Title 1 for E2E Process
            if pd.notna(row.get('Title 1')):
                e2e_name = str(row['Title 1']).strip()
                # E2E format: "10 Acquire to dispose", "65 Order to cash"
                if e2e_name and len(e2e_name) > 3:
                    # Extract number and name
                    parts = e2e_name.split(" ", 1)
                    if len(parts) == 2 and parts[0].isdigit():
                        e2e_code = parts[1].lower().replace(" ", "-")
                        current_e2e = e2e_name
                        
                        # Create or get E2E Process
                        e2e_obj = db.query(E2EProcess).filter(E2EProcess.code == e2e_code).first()
                        if not e2e_obj:
                            e2e_obj = E2EProcess(
                                code=e2e_code,
                                name=parts[1],
                                display_order=int(parts[0])
                            )
                            db.add(e2e_obj)
                            db.commit()
                            db.refresh(e2e_obj)
                            e2e_imported += 1
                            print(f"  E2E: {e2e_name}")
                        
                        current_e2e_obj = e2e_obj
            
            # Check Process Sequence ID for business processes
            seq_id = row.get('Process Sequence ID')
            if pd.notna(seq_id):
                process_code, sequence_num, full_seq = parse_process_sequence(seq_id)
                
                if process_code:
                    # Check if this is a business process (sequence_num == 0 or None)
                    # or a scenario (sequence_num > 0)
                    
                    if sequence_num == 0:
                        # This is a business process definition
                        # Get name from Title 3 (most common for process definitions)
                        process_name = None
                        
                        # Try Title 3 first (most common)
                        if pd.notna(row.get('Title 3')):
                            name = str(row['Title 3']).strip()
                            # Remove process code prefix if present
                            # Example: "65.05.040 Develop sales catalogs" -> "Develop sales catalogs"
                            if process_code in name:
                                process_name = name.replace(process_code, "").strip()
                            else:
                                process_name = name
                        
                        # Fallback to Title 2 or Title 4
                        if not process_name:
                            for title_col in ['Title 2', 'Title 4']:
                                if pd.notna(row.get(title_col)):
                                    name = str(row[title_col]).strip()
                                    if process_code in name:
                                        process_name = name.replace(process_code, "").strip()
                                        break
                        
                        if not process_name or not process_name.strip():
                            process_name = f"Process {process_code}"
                        
                        # Create or get Business Process
                        if current_e2e_obj:
                            bp = db.query(BusinessProcess).filter(BusinessProcess.process_code == process_code).first()
                            if not bp:
                                bp = BusinessProcess(
                                    process_code=process_code,
                                    name=process_name,
                                    e2e_process_id=current_e2e_obj.id,
                                    display_order=idx
                                )
                                db.add(bp)
                                db.commit()
                                db.refresh(bp)
                                processes_imported += 1
                                
                                if processes_imported % 50 == 0:
                                    print(f"  Imported {processes_imported} processes...")
                    
                    elif sequence_num and sequence_num > 0:
                        # This is a scenario (specific product implementation)
                        # Get business process
                        bp = db.query(BusinessProcess).filter(BusinessProcess.process_code == process_code).first()
                        
                        if bp:
                            # Get scenario name from Title 4
                            scenario_name = str(row.get('Title 4', '')).strip() if pd.notna(row.get('Title 4')) else None
                            
                            # Get product from Products column
                            product_str = row.get('Products')
                            erp_code = get_erp_code_from_product(product_str)
                            
                            if erp_code:
                                erp_system = db.query(ERPSystem).filter(ERPSystem.code == erp_code).first()
                                
                                if erp_system:
                                    # Check if scenario already exists
                                    existing = db.query(Scenario).filter(
                                        Scenario.scenario_code == full_seq,
                                        Scenario.erp_system_id == erp_system.id
                                    ).first()
                                    
                                    if not existing:
                                        if not scenario_name:
                                            scenario_name = f"{bp.name} in {erp_system.name}"
                                        
                                        scenario = Scenario(
                                            scenario_code=full_seq,
                                            business_process_id=bp.id,
                                            erp_system_id=erp_system.id,
                                            sequence_number=sequence_num,
                                            name=scenario_name
                                        )
                                        db.add(scenario)
                                        scenarios_imported += 1
                                        
                                        if scenarios_imported % 100 == 0:
                                            db.commit()
                                            print(f"  Imported {scenarios_imported} scenarios...")
        
        # Final commit
        db.commit()
        print(f"\n  [OK] Import complete:")
        print(f"    E2E Processes: {e2e_imported}")
        print(f"    Business Processes: {processes_imported}")
        print(f"    Scenarios: {scenarios_imported}")
        
        return processes_imported
        
    except Exception as e:
        print(f"  [ERROR] Error importing: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return 0

def main():
    """Main import function."""
    print("=" * 60)
    print("ITER - BPC Full Catalog Import")
    print("=" * 60)
    
    # Full catalog file
    catalog_file = Path(r"C:\DI_MOKSLAI\GO_FAST\Microsoft Business Process Catalog Full August 2025.xlsx")
    
    if not catalog_file.exists():
        print(f"[ERROR] File not found: {catalog_file}")
        return
    
    db = SessionLocal()
    
    try:
        import_full_catalog(catalog_file, db)
        
        # Print summary
        print("\n" + "=" * 60)
        print("Database Summary:")
        print("=" * 60)
        
        e2e_count = db.query(E2EProcess).count()
        bp_count = db.query(BusinessProcess).count()
        scenario_count = db.query(Scenario).count()
        erp_count = db.query(ERPSystem).count()
        
        print(f"E2E Processes: {e2e_count}")
        print(f"Business Processes: {bp_count}")
        print(f"Scenarios: {scenario_count}")
        print(f"ERP Systems: {erp_count}")
        
    except Exception as e:
        print(f"\n[ERROR] Import failed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

