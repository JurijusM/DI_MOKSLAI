# 🚀 ITER - Quick Start Guide

## ✅ What's Ready

All core code has been created:
- ✅ Database models (all tables)
- ✅ Database initialization script
- ✅ Streamlit app structure
- ✅ Process Selection page
- ✅ Data service for database access
- ✅ Seed script for initial data

## 📋 Setup Steps

### 1. Install Dependencies

```bash
cd C:\DI_MOKSLAI\ITER
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python database/init_db.py
```

This creates the SQLite database and all tables.

### 3. Seed Initial Data

```bash
python scripts/seed_database.py
```

This adds:
- 9 Microsoft ERP systems (BC, D365F, D365SCM, CRM, etc.)
- Test organization
- Test user

### 4. Run Streamlit App

```bash
cd streamlit_app
streamlit run app.py
```

Or use the multi-page app:

```bash
cd streamlit_app
streamlit run pages/1_🏠_Home.py
```

## 🎯 Current Features

### ✅ Working Now:
- Database schema created
- Streamlit app structure
- Home page
- Process Selection page (UI ready, needs BPC data import)
- Data service for database access

### ⏳ Next Steps:
1. **Import BPC Data**: Create script to import Excel files
2. **Dashboard**: Show progress statistics
3. **Recommendations**: Show BC vs D365F comparison, CRM decision
4. **Reports**: Export functionality

## 📁 Key Files

### Database:
- `database/init_db.py` - Initialize database
- `scripts/seed_database.py` - Add initial data

### Streamlit:
- `streamlit_app/app.py` - Main app (single-page)
- `streamlit_app/pages/1_🏠_Home.py` - Home page
- `streamlit_app/pages/2_📋_Process_Selection.py` - Process selection

### Services:
- `backend/app/services/recommendation_service.py` - Recommendation engine
- `streamlit_app/services/data_service.py` - Database access

## 🔧 Troubleshooting

### "No processes found"
- You need to import BPC data first
- Run: `python scripts/import_bpc_data.py` (when created)

### Database errors
- Make sure you ran `python database/init_db.py`
- Check that `database/iter.db` exists

### Import errors
- Make sure you're in the correct directory
- Check that all dependencies are installed

## 📝 Next: Import BPC Data

Once you have the BPC Excel files analyzed, create `scripts/import_bpc_data.py` to:
1. Parse Excel files from `C:\DI_MOKSLAI\GO_FAST\`
2. Extract processes and scenarios
3. Import into database

## 🎉 You're Ready!

The app structure is complete. You can:
1. Run the database initialization
2. Seed test data
3. Start the Streamlit app
4. Begin building the import script for BPC data



