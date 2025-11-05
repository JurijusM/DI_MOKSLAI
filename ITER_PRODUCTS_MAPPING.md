# ITER - Microsoft Products Mapping

## Products to be Analyzed from BPC Files

Based on the user's requirements, we need to identify and map all Microsoft products mentioned in the BPC Excel files.

## Expected Products

### Primary ERP Products
| Code | Full Name | Category | Notes |
|------|-----------|----------|-------|
| **BC** | Dynamics 365 Business Central | ERP | Mid-market ERP solution |
| **D365F** | Dynamics 365 Finance | ERP | Enterprise financial management |
| **D365SCM** | Dynamics 365 Supply Chain Management | ERP | Supply chain & manufacturing |
| **D365COMM** | Dynamics 365 Commerce | ERP | E-commerce & retail |

### CRM Products
| Code | Full Name | Category | Notes |
|------|-----------|----------|-------|
| **CRM** | Dynamics 365 Sales | CRM | Customer relationship management |
| **D365CS** | Dynamics 365 Customer Service | CRM | Customer service management |
| **D365FS** | Dynamics 365 Field Service | CRM | Field service management |

### Specialized Products
| Code | Full Name | Category | Notes |
|------|-----------|----------|-------|
| **D365PO** | Dynamics 365 Project Operations | Specialized | Project management |
| **D365HR** | Dynamics 365 Human Resources | Specialized | HR management |

## Scenario Code Mapping

Based on the example provided:
- Process: `65.05.040` = "Develop sales catalogs"
- Scenario: `65.05.040.100` = D365 Supply Chain Management implementation
- Scenario: `65.05.040.101` = Business Central implementation

**Pattern**: `XX.XX.XXX.XXX` where the last segment maps to a product.

## Recommendation Logic

### After Discovery Completion

1. **Primary ERP Selection**:
   - Compare: BC vs D365F vs D365SCM vs D365COMM
   - Select highest scoring product
   - Display: Score, Coverage %, Gaps

2. **CRM Decision**:
   - Check if any CRM product (CRM, D365CS, D365FS) has score ≥ 50%
   - If yes: "CRM Needed" with best CRM product
   - If no: "CRM Not Required"

3. **Additional Products**:
   - List any specialized products with score ≥ 50%
   - Include rationale for each

## Next Step

**Run Analysis Script**:
```bash
python scripts/analyze_bpc_products.py
```

This will:
1. Scan all BPC Excel files
2. Identify all mentioned Microsoft products
3. Map scenario codes to products
4. Generate complete product list

Once analysis is complete, we'll update this document with actual products found.



