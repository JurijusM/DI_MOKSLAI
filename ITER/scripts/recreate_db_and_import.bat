@echo off
echo ============================================================
echo ITER - Recreate Database and Import Hierarchy
echo ============================================================
echo.
echo WARNING: Make sure Streamlit is stopped first!
echo Press Ctrl+C to cancel, or
pause

echo.
echo Step 1: Removing old database...
del /F /Q "C:\DI_MOKSLAI\ITER\database\iter.db" 2>nul
echo [OK] Database removed

echo.
echo Step 2: Creating new database...
python database/init_db.py

echo.
echo Step 3: Seeding ERP systems...
python scripts/seed_database.py

echo.
echo Step 4: Importing hierarchy...
python scripts/import_hierarchy.py

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next: Start Streamlit
echo   cd streamlit_app
echo   streamlit run app.py
pause
















