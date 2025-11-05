# ITER - Intelligent Technology Evaluation & Requirements

Self-Service ERP Requirements Gathering Platform

## Project Structure

```
ITER/
├── backend/                    # Backend application (FastAPI - optional)
│   └── app/
│       ├── models/            # SQLAlchemy database models
│       ├── services/          # Business logic
│       ├── controllers/       # API controllers
│       ├── utils/             # Utility functions
│       └── schemas/           # Pydantic schemas
│
├── streamlit_app/              # Streamlit frontend (main UI)
│   ├── pages/                 # Multi-page Streamlit app
│   │   ├── 1_🏠_Home.py
│   │   ├── 2_📋_Process_Selection.py
│   │   ├── 3_📊_Dashboard.py
│   │   ├── 4_🎯_Recommendations.py
│   │   └── 5_📄_Reports.py
│   ├── components/            # Reusable Streamlit components
│   ├── services/              # Data access services
│   ├── utils/                 # Utility functions
│   └── .streamlit/            # Streamlit configuration
│
├── database/                  # Database files and migrations
│   ├── init_db.py            # Database initialization
│   └── schema.sql             # SQL schema
│
├── scripts/                    # Utility scripts
│   ├── analyze_bpc_products.py
│   ├── import_bpc_data.py
│   └── seed_database.py
│
├── docs/                      # Additional documentation
│
├── tests/                     # Test files
│
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize database:**
   ```bash
   python database/init_db.py
   ```

3. **Run Streamlit app:**
   ```bash
   cd streamlit_app
   streamlit run app.py
   ```

## Documentation

See main documentation in parent directory:
- `ITER_PROJECT_PLAN.md` - Complete project plan
- `ITER_PYTHON_ARCHITECTURE.md` - Technical architecture
- `ITER_PYTHON_STACK_SUMMARY.md` - Quick reference



