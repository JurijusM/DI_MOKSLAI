"""
Script to analyze BPC Excel files and identify all Microsoft ERP products mentioned.
This will help us understand what products need to be supported in ITER.
"""

import os
import pandas as pd
import re
from pathlib import Path
from collections import defaultdict, Counter

# Path to BPC files
BPC_DIR = Path(r"C:\DI_MOKSLAI\GO_FAST")

# Known Microsoft products and their variations
PRODUCT_PATTERNS = {
    'Business Central': [
        r'business central',
        r'dynamics 365 business central',
        r'd365 bc',
        r'bc\b'
    ],
    'D365 Finance': [
        r'dynamics 365 finance',
        r'd365 finance',
        r'd365f\b',
        r'finance and operations',
        r'f&o\b'
    ],
    'D365 Supply Chain': [
        r'dynamics 365 supply chain',
        r'supply chain management',
        r'd365 scm',
        r'scm\b'
    ],
    'D365 Commerce': [
        r'dynamics 365 commerce',
        r'd365 commerce'
    ],
    'D365 Sales (CRM)': [
        r'dynamics 365 sales',
        r'd365 sales',
        r'customer relationship management',
        r'crm\b'
    ],
    'D365 Customer Service': [
        r'dynamics 365 customer service',
        r'customer service'
    ],
    'D365 Field Service': [
        r'dynamics 365 field service',
        r'field service'
    ],
    'D365 Project Operations': [
        r'dynamics 365 project operations',
        r'project operations'
    ],
    'D365 Human Resources': [
        r'dynamics 365 human resources',
        r'human resources',
        r'hr\b'
    ]
}

def find_products_in_text(text):
    """Find all products mentioned in a text string."""
    if pd.isna(text):
        return []
    
    text = str(text).lower()
    found_products = set()
    
    for product, patterns in PRODUCT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found_products.add(product)
                break
    
    return list(found_products)

def analyze_excel_file(file_path):
    """Analyze a single Excel file for product mentions."""
    print(f"\n{'='*60}")
    print(f"Analyzing: {file_path.name}")
    print('='*60)
    
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        all_products = []
        scenario_products = defaultdict(list)
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Look for scenario codes (format: XX.XX.XXX.XXX)
            scenario_pattern = r'(\d+\.\d+\.\d+\.\d+)'
            
            # Search through all columns
            for col in df.columns:
                for idx, value in df[col].items():
                    if pd.notna(value):
                        value_str = str(value)
                        
                        # Check if this looks like a scenario row
                        if re.search(scenario_pattern, value_str):
                            # Extract scenario code
                            match = re.search(scenario_pattern, value_str)
                            if match:
                                scenario_code = match.group(1)
                                # Find products in this row
                                row_products = []
                                for cell_value in df.loc[idx]:
                                    if pd.notna(cell_value):
                                        products = find_products_in_text(str(cell_value))
                                        row_products.extend(products)
                                
                                if row_products:
                                    scenario_products[scenario_code].extend(row_products)
                        
                        # Also search column names and all cells
                        products = find_products_in_text(value_str)
                        all_products.extend(products)
        
        return all_products, scenario_products
        
    except Exception as e:
        print(f"Error reading {file_path.name}: {e}")
        return [], {}

def main():
    """Main function to analyze all BPC files."""
    print("="*60)
    print("ITER - BPC Product Analysis")
    print("="*60)
    
    # Get all Excel files
    excel_files = list(BPC_DIR.glob("*.xlsx"))
    excel_files = [f for f in excel_files if not f.name.startswith("~$")]
    
    print(f"\nFound {len(excel_files)} Excel files to analyze")
    
    all_products_found = []
    all_scenario_products = defaultdict(list)
    
    # Analyze each file
    for file_path in excel_files:
        products, scenario_products = analyze_excel_file(file_path)
        all_products_found.extend(products)
        
        for scenario, products_list in scenario_products.items():
            all_scenario_products[scenario].extend(products_list)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    product_counts = Counter(all_products_found)
    print("\nProducts found (by frequency):")
    for product, count in product_counts.most_common():
        print(f"  {product}: {count} mentions")
    
    print(f"\nUnique products: {len(product_counts)}")
    print(f"\nProducts list:")
    for product in sorted(product_counts.keys()):
        print(f"  - {product}")
    
    # Scenario mapping summary
    print(f"\n\nScenario-to-Product Mappings Found: {len(all_scenario_products)}")
    print("\nSample scenario mappings (first 10):")
    for i, (scenario, products) in enumerate(list(all_scenario_products.items())[:10]):
        unique_products = list(set(products))
        print(f"  {scenario}: {', '.join(unique_products)}")
    
    # Generate product list for database
    print("\n" + "="*60)
    print("RECOMMENDED PRODUCT LIST FOR DATABASE")
    print("="*60)
    
    unique_products = sorted(set(all_products_found))
    for i, product in enumerate(unique_products, 1):
        code = product.replace('D365 ', '').replace('Dynamics 365 ', '').replace(' ', '_').upper()
        if code == 'BUSINESS_CENTRAL':
            code = 'BC'
        elif code == 'D365_SALES_(CRM)':
            code = 'CRM'
        elif code == 'D365_FINANCE':
            code = 'D365F'
        elif code == 'D365_SUPPLY_CHAIN':
            code = 'D365SCM'
        elif code == 'D365_COMMERCE':
            code = 'D365COMM'
        elif code == 'D365_CUSTOMER_SERVICE':
            code = 'D365CS'
        elif code == 'D365_FIELD_SERVICE':
            code = 'D365FS'
        elif code == 'D365_PROJECT_OPERATIONS':
            code = 'D365PO'
        elif code == 'D365_HUMAN_RESOURCES':
            code = 'D365HR'
        
        print(f"{i}. Code: {code:<15} Name: {product}")
    
    return unique_products, all_scenario_products

if __name__ == "__main__":
    products, scenarios = main()



