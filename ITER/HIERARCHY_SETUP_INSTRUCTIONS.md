# ITER - Hierarchical Setup Instructions

## ✅ What's Been Updated

The system now supports **full hierarchical tree structure** with MoSCoW prioritization at the **lowest level** (work items).

### New Structure:

```
Level 1 (Title 1): E2E Process
└─ Level 2 (Title 2): Process Area
   └─ Level 3 (Title 3): Business Process
      └─ Level 4 (Title 4): Scenario (product-specific)
         └─ Work Items: Task, Configuration deliverable, Workshop, etc.
                        ↑
                    SELECT MoSCoW HERE
```

### Work Item Types (Lowest Level):
- Task
- Configuration deliverable  
- Workshop
- Document deliverable

Users select **Must/Should/Could/Won't** on these work items, then the system:
1. Rolls up to scenarios
2. Maps scenarios to Microsoft products (BC, D365F, D365SCM, etc.)
3. Recommends products based on coverage

---

## 🛠️ Setup Steps

### Important: Stop Streamlit First!

If Streamlit is running, **stop it** (Ctrl+C) before recreating the database.

### Option A: Run Batch File (Easiest)

```bash
cd C:\DI_MOKSLAI\ITER\scripts
recreate_db_and_import.bat
```

This will:
1. Remove old database
2. Create new schema with hierarchy tables
3. Seed ERP systems
4. Import full BPC hierarchy

### Option B: Manual Steps

```bash
cd C:\DI_MOKSLAI\ITER

# 1. Stop Streamlit (Ctrl+C in Streamlit terminal)

# 2. Remove old database
del database\iter.db

# 3. Initialize database
python database/init_db.py

# 4. Seed ERP systems
python scripts/seed_database.py

# 5. Import hierarchy
python scripts/import_hierarchy.py

# 6. Start Streamlit
cd streamlit_app
streamlit run app.py
```

---

## 📊 New Tables Created

- `process_hierarchy` - Full Title 1-5 hierarchy (7,983 items)
- `hierarchy_requirements` - MoSCoW selections on work items
- `work_items` - Alternative table (optional)
- `work_item_requirements` - Alternative table (optional)

---

## 🎯 New Features

### 1. Tree View UI
- Expand/collapse navigation (▶/▼)
- Full hierarchy: E2E → Area → Process → Scenario → Work Items
- MoSCoW selection at lowest level only

### 2. Recommendations
- Compares BC vs D365F vs D365SCM vs D365COMM
- CRM decision (Yes/No) with best CRM product
- Additional specialized products

### 3. Dashboard
- Shows Must/Should/Could/Won't counts
- Progress tracking
- Work items evaluated

---

## 📁 New Files Created

### Models:
- `backend/app/models/hierarchy.py` - ProcessHierarchy, HierarchyRequirement
- `backend/app/models/work_item.py` - WorkItem, WorkItemRequirement

### Services:
- `backend/app/services/hierarchy_recommendation_service.py` - Recommendation engine
- `streamlit_app/services/hierarchy_service.py` - Data access

### Scripts:
- `scripts/import_hierarchy.py` - Import full BPC hierarchy
- `scripts/recreate_db_and_import.bat` - One-click setup

### UI:
- `streamlit_app/components/tree_view.py` - Tree component
- `streamlit_app/pages/2_📋_Process_Selection.py` - Updated with tree view
- `streamlit_app/pages/3_📊_Dashboard.py` - Updated dashboard
- `streamlit_app/pages/4_🎯_Recommendations.py` - Recommendations page

---

## 🚀 Next Steps

1. **Stop Streamlit** (if running)
2. **Run batch file**: `scripts\recreate_db_and_import.bat`
3. **Start Streamlit**: `cd streamlit_app && streamlit run app.py`
4. **Test**:
   - Navigate hierarchy in Process Selection
   - Select MoSCoW on work items
   - View recommendations

---

## 📝 Example: How to Use

1. Open ITER in browser (http://localhost:8501)
2. Go to "Process Selection"
3. Select E2E process: "Order to cash"
4. Expand hierarchy:
   ```
   ▼ 65 Order to cash
     ▼ 65.05 Sales management
       ▼ 65.05.040 Develop sales catalogs
         ▼ 65.05.040.100 Develop catalogs in D365 SCM
           ○ Configuration deliverable [Must] ← Select here
           ○ Task [Should] ← Select here
   ```
5. Save selections
6. Go to "Recommendations" to see BC vs D365F comparison

---

## ✅ Status

All core components ready:
- ✅ Database schema updated
- ✅ Models created
- ✅ Import script ready
- ✅ Tree UI component ready
- ✅ Recommendation service updated
- ✅ All pages updated

**Ready to test!**
















