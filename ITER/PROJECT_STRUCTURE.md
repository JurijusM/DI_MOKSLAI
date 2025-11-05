# ITER - Project Structure Overview

## Complete Directory Tree

```
ITER/
│
├── backend/                           # Backend application (FastAPI - optional)
│   └── app/
│       ├── models/                   # SQLAlchemy database models
│       │   ├── __init__.py
│       │   ├── organization.py      # Organization model
│       │   ├── user.py              # User model
│       │   ├── process.py           # E2E Process & Business Process models
│       │   ├── scenario.py          # Scenario model
│       │   ├── requirement.py       # CustomerRequirement model
│       │   └── product.py           # ERPSystem model
│       │
│       ├── services/                 # Business logic services
│       │   ├── __init__.py
│       │   ├── recommendation_service.py  ✅ Created
│       │   ├── process_service.py
│       │   ├── requirement_service.py
│       │   └── import_service.py
│       │
│       ├── controllers/               # API controllers (if using FastAPI)
│       ├── schemas/                   # Pydantic schemas
│       ├── utils/                     # Utility functions
│       └── migrations/                # Alembic migrations
│
├── streamlit_app/                     # Streamlit frontend (main UI)
│   ├── pages/                         # Multi-page Streamlit app
│   │   ├── 1_🏠_Home.py             # Welcome page
│   │   ├── 2_📋_Process_Selection.py # Main feature - select priorities
│   │   ├── 3_📊_Dashboard.py         # Progress tracking
│   │   ├── 4_🎯_Recommendations.py   # Product recommendations (BC vs D365F, CRM)
│   │   └── 5_📄_Reports.py           # Export & fit/gap analysis
│   │
│   ├── components/                    # Reusable Streamlit components
│   │   ├── __init__.py
│   │   ├── process_card.py           # Display process card
│   │   ├── priority_selector.py      # Must/Should/Optional selector
│   │   ├── progress_chart.py          # Progress visualization
│   │   └── recommendation_card.py     # Product recommendation display
│   │
│   ├── services/                      # Data access services
│   │   ├── auth_service.py           # Authentication
│   │   └── data_service.py            # Database access
│   │
│   ├── utils/                         # Utility functions
│   │   └── session_state.py          # Streamlit session management
│   │
│   ├── .streamlit/                    # Streamlit configuration
│   │   ├── config.toml               ✅ Created
│   │   └── secrets.toml              # Secrets (not in git)
│   │
│   └── app.py                         # Main Streamlit entry point
│
├── database/                          # Database files and migrations
│   ├── init_db.py                    # Database initialization script
│   ├── schema.sql                     # SQL schema file
│   └── iter.db                        # SQLite database (created at runtime)
│
├── scripts/                           # Utility scripts
│   ├── README.md                      ✅ Created
│   ├── analyze_bpc_products.py      ✅ Created - Analyze Excel files
│   ├── import_bpc_data.py            # Import BPC Excel data to database
│   └── seed_database.py              # Seed initial data
│
├── docs/                              # Additional documentation
│   ├── API.md                         # API documentation
│   └── USER_GUIDE.md                  # User guide
│
├── tests/                             # Test files
│   ├── test_recommendations.py
│   └── test_import.py
│
├── .gitignore                         ✅ Created
├── requirements.txt                   ✅ Created - Python dependencies
├── README.md                          ✅ Created
└── PROJECT_STRUCTURE.md               # This file
```

## Key Directories Explained

### `backend/app/`
- **Purpose**: Core application logic (optional FastAPI backend)
- **Models**: Database models using SQLAlchemy
- **Services**: Business logic (recommendation engine, data processing)
- **Note**: Streamlit can directly access database, FastAPI is optional

### `streamlit_app/`
- **Purpose**: Main user interface
- **pages/**: Multi-page Streamlit app (navigation via sidebar)
- **components/**: Reusable UI components
- **services/**: Data access layer

### `database/`
- **Purpose**: Database files and schema
- **init_db.py**: Initialize database with schema
- **schema.sql**: SQL schema definition
- **iter.db**: SQLite database (created on first run)

### `scripts/`
- **Purpose**: Utility scripts for data import and analysis
- **analyze_bpc_products.py**: Analyze BPC Excel files to find products
- **import_bpc_data.py**: Import BPC data to database
- **seed_database.py**: Seed ERP systems and test data

## File Naming Conventions

- **Models**: `snake_case.py` (e.g., `business_process.py`)
- **Services**: `snake_case_service.py` (e.g., `recommendation_service.py`)
- **Streamlit pages**: Numbered with emoji for navigation (e.g., `1_🏠_Home.py`)
- **Components**: `snake_case.py` (e.g., `process_card.py`)

## Development Workflow

1. **Database Setup**:
   ```bash
   python database/init_db.py
   ```

2. **Import BPC Data**:
   ```bash
   python scripts/import_bpc_data.py
   ```

3. **Run Streamlit App**:
   ```bash
   cd streamlit_app
   streamlit run app.py
   ```

4. **Run Tests**:
   ```bash
   pytest tests/
   ```

## Next Steps

1. Create database models in `backend/app/models/`
2. Create database initialization script in `database/init_db.py`
3. Build first Streamlit page: `streamlit_app/pages/2_📋_Process_Selection.py`
4. Create Excel parser: `scripts/import_bpc_data.py`



