"""
Import BPC Data - Import Microsoft Business Process Catalog data from Excel files
"""

import sys
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook

# Add ITER directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.database import SessionLocal
from backend.app.models import E2EProcess, BusinessProcess, Scenario, ERPSystem

def get_e2e_process_name_from_filename(filename: str) -> str:
    """Extract E2E process name from filename."""
    # Example: "BPC - Order to Cash August 2025.xlsx" -> "Order to Cash"
    name = filename.replace("BPC - ", "").replace(" August 2025.xlsx", "")
    name = name.replace(".xlsx", "")
    return name.strip()

def get_e2e_process_code_from_name(name: str) -> str:
    """Convert E2E process name to code."""
    # Example: "Order to Cash" -> "order-to-cash"
    return name.lower().replace(" ", "-")

def parse_scenario_code(scenario_str: str) -> tuple:
    """
    Parse scenario code like "65.05.040.100" into:
    - process_code: "65.05.040"
    - sequence_number: 100
    - erp_system_id: determined by sequence number
    """
    if pd.isna(scenario_str):
        return None, None, None
    
    scenario_str = str(scenario_str).strip()
    
    # Check if it matches pattern XX.XX.XXX.XXX
    parts = scenario_str.split(".")
    if len(parts) != 4:
        return None, None, None
    
    try:
        process_code = ".".join(parts[:3])  # "65.05.040"
        sequence_number = int(parts[3])     # 100, 101, etc.
        
        # Map sequence numbers to ERP systems (common patterns)
        # This is a simplified mapping - adjust based on actual BPC data
        erp_mapping = {
            100: "D365SCM",  # Dynamics 365 Supply Chain Management
            101: "BC",       # Business Central
            102: "D365F",    # D365 Finance
            103: "CRM",      # D365 Sales/CRM
            104: "D365COMM", # D365 Commerce
            # Add more mappings as needed
        }
        
        # Get ERP system code from sequence number
        erp_code = erp_mapping.get(sequence_number)
        
        return process_code, sequence_number, erp_code
    except (ValueError, IndexError):
        return None, None, None

def import_excel_file(file_path: Path, db):
    """Import data from a single BPC Excel file."""
    print(f"\nProcessing: {file_path.name}")
    
    try:
        # Get E2E process name from filename
        e2e_name = get_e2e_process_name_from_filename(file_path.name)
        e2e_code = get_e2e_process_code_from_name(e2e_name)
        
        print(f"  E2E Process: {e2e_name} ({e2e_code})")
        
        # Create or get E2E Process
        e2e_process = db.query(E2EProcess).filter(E2EProcess.code == e2e_code).first()
        if not e2e_process:
            e2e_process = E2EProcess(
                code=e2e_code,
                name=e2e_name,
                display_order=1
            )
            db.add(e2e_process)
            db.commit()
            db.refresh(e2e_process)
            print(f"  Created E2E Process: {e2e_name}")
        
        # Read Excel file
        workbook = load_workbook(file_path, data_only=True)
        sheet = workbook.active  # Use first sheet
        
        # Convert to DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet.title)
        
        print(f"  Found {len(df)} rows")
        
        # Look for process columns based on actual Excel structure
        # Columns: 'Process Sequence ID', 'Title 1', 'Title 2', 'Products', etc.
        process_code_col = "Process Sequence ID"
        process_name_col = None
        products_col = "Products"
        
        # Try to find title column (usually Title 1 or Title 2)
        for col in df.columns:
            if "Title" in str(col) and "1" in str(col):
                process_name_col = col
                break
        
        if not process_name_col:
            # Fallback to Title 2 or Description
            for col in df.columns:
                if "Title" in str(col):
                    process_name_col = col
                    break
        
        if not process_name_col:
            process_name_col = "Description"
        
        if process_code_col not in df.columns:
            print(f"  [WARNING] Could not find 'Process Sequence ID' column in {file_path.name}")
            return 0
        
        processes_imported = 0
        scenarios_imported = 0
        
        # Process each row
        for idx, row in df.iterrows():
            process_code_raw = row[process_code_col] if pd.notna(row[process_code_col]) else None
            process_name_raw = row[process_name_col] if pd.notna(row[process_name_col]) else None
            
            if pd.isna(process_code_raw):
                continue
            
            process_code = str(process_code_raw).strip()
            process_name = str(process_name_raw).strip() if pd.notna(process_name_raw) else "Unnamed Process"
            
            # Skip if no process code or invalid format
            if not process_code or process_code == "nan" or process_code.lower() == "none":
                continue
            
            # Process Sequence ID might be in format XX.XX.XXX or just a number
            # Try to extract process code format
            if "." in process_code and len(process_code.split(".")) == 3:
                # Already in correct format
                pass
            elif "." in process_code:
                # Might have more parts - take first 3
                parts = process_code.split(".")
                if len(parts) >= 3:
                    process_code = ".".join(parts[:3])
                else:
                    continue  # Skip invalid format
            else:
                # Might just be a number or ID, skip for now
                continue
            
            # Create or get Business Process
            bp = db.query(BusinessProcess).filter(BusinessProcess.process_code == process_code).first()
            if not bp:
                bp = BusinessProcess(
                    process_code=process_code,
                    name=process_name,
                    e2e_process_id=e2e_process.id,
                    description=None,
                    display_order=idx + 1
                )
                db.add(bp)
                db.commit()
                db.refresh(bp)
                processes_imported += 1
            else:
                # Process exists, commit any pending changes
                db.commit()
            
            # Try to find and import scenarios from Products column
            if products_col in df.columns and pd.notna(row[products_col]):
                products_str = str(row[products_col]).strip()
                # Products column might contain product names - parse them
                # Example: "Dynamics 365 Business Central, Dynamics 365 Finance"
                products_list = [p.strip() for p in products_str.split(",") if p.strip()]
                
                for product_name in products_list:
                    # Map product names to codes
                    product_map = {
                        "Dynamics 365 Business Central": "BC",
                        "Business Central": "BC",
                        "Dynamics 365 Finance": "D365F",
                        "D365 Finance": "D365F",
                        "Dynamics 365 Supply Chain Management": "D365SCM",
                        "D365 Supply Chain": "D365SCM",
                        "Supply Chain Management": "D365SCM",
                        "Dynamics 365 Commerce": "D365COMM",
                        "D365 Commerce": "D365COMM",
                        "Dynamics 365 Sales": "CRM",
                        "D365 Sales": "CRM",
                        "Dynamics 365 Customer Service": "D365CS",
                        "D365 Customer Service": "D365CS",
                        "Dynamics 365 Field Service": "D365FS",
                        "D365 Field Service": "D365FS",
                        "Dynamics 365 Project Operations": "D365PO",
                        "D365 Project Operations": "D365PO",
                        "Dynamics 365 Human Resources": "D365HR",
                        "D365 Human Resources": "D365HR",
                    }
                    
                    erp_code = None
                    for key, code in product_map.items():
                        if key.lower() in product_name.lower():
                            erp_code = code
                            break
                    
                    if erp_code:
                        erp_system = db.query(ERPSystem).filter(ERPSystem.code == erp_code).first()
                        if erp_system:
                            # Check if scenario already exists for this process + ERP
                            existing = db.query(Scenario).filter(
                                Scenario.business_process_id == bp.id,
                                Scenario.erp_system_id == erp_system.id
                            ).first()
                            
                            if not existing:
                                # Create scenario code (process_code + sequence)
                                # Use a simple sequence: 100 for first product, 101 for second, etc.
                                existing_scenarios_count = db.query(Scenario).filter(
                                    Scenario.business_process_id == bp.id
                                ).count()
                                
                                sequence_num = 100 + existing_scenarios_count
                                scenario_code = f"{process_code}.{sequence_num}"
                                
                                scenario = Scenario(
                                    scenario_code=scenario_code,
                                    business_process_id=bp.id,
                                    erp_system_id=erp_system.id,
                                    sequence_number=sequence_num,
                                    name=f"{process_name} in {erp_system.name}"
                                )
                                db.add(scenario)
                                db.flush()  # Flush to check for errors before commit
                                scenarios_imported += 1
        
        try:
            db.commit()
            print(f"  [OK] Imported {processes_imported} processes, {scenarios_imported} scenarios")
        except Exception as e:
            db.rollback()
            print(f"  [WARNING] Some scenarios failed: {e}")
            # Try to commit just the processes
            try:
                db.commit()
                print(f"  [OK] Imported {processes_imported} processes (some scenarios skipped)")
            except:
                pass
        
        return processes_imported
        
    except Exception as e:
        print(f"  [ERROR] Error importing {file_path.name}: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return 0

def main():
    """Main import function."""
    print("=" * 60)
    print("ITER - BPC Data Import")
    print("=" * 60)
    
    # BPC files directory
    bpc_dir = Path(r"C:\DI_MOKSLAI\GO_FAST")
    
    if not bpc_dir.exists():
        print(f"[ERROR] Directory not found: {bpc_dir}")
        return
    
    # Find all BPC Excel files
    excel_files = list(bpc_dir.glob("BPC - *.xlsx"))
    excel_files = [f for f in excel_files if not f.name.startswith("~$")]
    
    print(f"\nFound {len(excel_files)} BPC Excel files")
    
    if not excel_files:
        print("[ERROR] No BPC Excel files found!")
        return
    
    db = SessionLocal()
    total_processes = 0
    
    try:
        for excel_file in excel_files:
            imported = import_excel_file(excel_file, db)
            total_processes += imported
        
        print("\n" + "=" * 60)
        print(f"[OK] Import complete!")
        print(f"Total processes imported: {total_processes}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] Import failed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

