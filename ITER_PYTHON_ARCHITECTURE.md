# ITER - Python + Streamlit Architecture

## Technology Stack Decision

✅ **Backend**: Python 3.11+ with FastAPI  
✅ **Frontend**: Streamlit (for rapid UI development)  
✅ **Database**: SQLite (development) / PostgreSQL (production)  
✅ **Excel Processing**: openpyxl / pandas  

## Why Streamlit?

**Advantages:**
- ✅ Fast development - UI built with Python, no separate frontend
- ✅ Perfect for internal tools and self-service portals
- ✅ Built-in authentication support
- ✅ Easy integration with pandas for data analysis
- ✅ Quick prototyping and iteration
- ✅ Good for forms and dashboards (perfect for requirements gathering)

**Considerations:**
- Multi-page apps work well
- Can be styled with custom CSS if needed
- Supports file uploads (for future BPC file imports)
- Easy to deploy (streamlit cloud or docker)

## Project Structure

```
ITER/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app (for API endpoints if needed)
│   │   ├── config.py               # Configuration
│   │   ├── database.py             # Database connection & models
│   │   ├── models/                 # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── organization.py
│   │   │   ├── user.py
│   │   │   ├── process.py
│   │   │   ├── requirement.py
│   │   │   └── recommendation.py
│   │   ├── services/               # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── process_service.py
│   │   │   ├── requirement_service.py
│   │   │   ├── recommendation_service.py
│   │   │   └── import_service.py
│   │   ├── utils/                  # Utilities
│   │   │   ├── __init__.py
│   │   │   ├── excel_parser.py
│   │   │   └── validators.py
│   │   └── schemas/                # Pydantic schemas
│   │       ├── __init__.py
│   │       ├── process.py
│   │       └── requirement.py
│   ├── migrations/                 # Alembic migrations
│   ├── scripts/
│   │   ├── analyze_products.py     # Analyze BPC files
│   │   ├── import_bpc_data.py      # Import Excel files
│   │   └── seed_database.py        # Seed initial data
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── streamlit_app/
│   ├── pages/
│   │   ├── 1_🏠_Home.py
│   │   ├── 2_📋_Process_Selection.py
│   │   ├── 3_📊_Dashboard.py
│   │   ├── 4_🎯_Recommendations.py
│   │   └── 5_📄_Reports.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── process_card.py
│   │   ├── priority_selector.py
│   │   ├── progress_chart.py
│   │   └── recommendation_card.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── data_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── session_state.py
│   ├── .streamlit/
│   │   └── config.toml
│   ├── app.py                      # Main Streamlit entry point
│   └── requirements.txt
│
├── database/
│   ├── init_db.py                  # Initialize database
│   └── schema.sql                  # SQL schema
│
├── docs/
├── .env.example
├── README.md
└── docker-compose.yml
```

## Microsoft Products to Support

Based on BPC analysis, we need to support:

| Code | Full Name | Description |
|------|-----------|-------------|
| **BC** | Dynamics 365 Business Central | Mid-market ERP |
| **D365F** | Dynamics 365 Finance | Enterprise financial management |
| **D365SCM** | Dynamics 365 Supply Chain Management | Supply chain & manufacturing |
| **D365COMM** | Dynamics 365 Commerce | E-commerce & retail |
| **CRM** | Dynamics 365 Sales (CRM) | Customer relationship management |
| **D365CS** | Dynamics 365 Customer Service | Customer service management |
| **D365FS** | Dynamics 365 Field Service | Field service management |
| **D365PO** | Dynamics 365 Project Operations | Project management |
| **D365HR** | Dynamics 365 Human Resources | HR management |

*Note: Actual products will be determined after analyzing BPC files*

## Recommendation Engine Logic

### Scoring Algorithm

```python
def calculate_product_recommendations(organization_id: str):
    """
    Calculate recommendation scores for each Microsoft product.
    """
    # 1. Get organization's requirements
    must_requirements = get_must_requirements(organization_id)
    should_requirements = get_should_requirements(organization_id)
    
    recommendations = {}
    
    for product in MICROSOFT_PRODUCTS:
        # 2. Find scenarios that cover requirements
        must_coverage = calculate_coverage(must_requirements, product)
        should_coverage = calculate_coverage(should_requirements, product)
        
        # 3. Calculate scores
        must_score = must_coverage * 100  # 0-100
        should_score = should_coverage * 50  # Weighted lower
        
        # 4. Total score (must is 70%, should is 30%)
        total_score = (must_score * 0.7) + (should_score * 0.3)
        
        # 5. Identify gaps
        gaps = find_missing_requirements(must_requirements, product)
        
        recommendations[product] = {
            'score': total_score,
            'must_coverage': must_coverage,
            'should_coverage': should_coverage,
            'gaps': gaps,
            'recommendation': get_recommendation_level(total_score)
        }
    
    return recommendations

def get_recommendation_level(score: float) -> str:
    """Get recommendation level based on score."""
    if score >= 85:
        return "Highly Recommended"
    elif score >= 70:
        return "Recommended"
    elif score >= 50:
        return "Consider"
    else:
        return "Not Recommended"
```

### Decision Logic

After discovery completion:
1. **Primary ERP Selection**: Compare BC vs D365 Finance vs D365 SCM
2. **CRM Need**: Check if CRM requirements exist
3. **Additional Products**: Recommend other products based on gaps

Example output:
```
Primary Recommendation: Dynamics 365 Business Central (Score: 87%)
CRM Needed: Yes (Score: 78%)
Additional Products: 
  - Dynamics 365 Commerce (Score: 65%) - Recommended for e-commerce needs
```

## Streamlit App Pages

### 1. Home Page
- Welcome message
- Progress overview
- Quick links to other pages
- Organization info

### 2. Process Selection (Main Page)
- Filter by E2E Process
- List of business processes
- Priority selector for each process (Must/Should/Optional/Not Needed)
- Search and filter
- Save progress indicator

### 3. Dashboard
- Completion percentage
- Statistics (Must/Should/Optional counts)
- Progress chart
- Last updated timestamp
- Quick actions

### 4. Recommendations
- Product recommendation cards with scores
- Comparison view
- Coverage breakdown
- Gaps identified
- Decision summary

### 5. Reports
- Fit/gap analysis
- Export to Excel/PDF
- Detailed requirement list
- Recommendation rationale

## Database Schema (SQLite/PostgreSQL)

```sql
-- ERP Systems (Microsoft Products)
CREATE TABLE erp_systems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(20) UNIQUE NOT NULL,  -- 'BC', 'D365F', 'CRM', etc.
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50),  -- 'ERP', 'CRM', 'Specialized'
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scenarios with product mapping
CREATE TABLE scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_code VARCHAR(50) NOT NULL,  -- '65.05.040.100'
    business_process_id INTEGER REFERENCES business_processes(id),
    erp_system_id INTEGER REFERENCES erp_systems(id),
    name VARCHAR(255),
    description TEXT,
    sequence_number INTEGER,  -- 100, 101, etc.
    UNIQUE(scenario_code, erp_system_id)
);

-- Product Recommendations
CREATE TABLE product_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER REFERENCES organizations(id),
    erp_system_id INTEGER REFERENCES erp_systems(id),
    recommendation_score DECIMAL(5,2),
    must_coverage_percentage DECIMAL(5,2),
    should_coverage_percentage DECIMAL(5,2),
    recommendation_level VARCHAR(50),  -- 'Highly Recommended', 'Recommended', etc.
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, erp_system_id)
);
```

## Key Python Packages

```txt
# Backend
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pydantic==2.5.0
python-dotenv==1.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Data Processing
pandas==2.1.3
openpyxl==3.1.2
numpy==1.26.2

# Streamlit
streamlit==1.28.1
streamlit-authenticator==0.2.3
plotly==5.18.0  # For charts

# Database
sqlite3  # Built-in (dev)
psycopg2-binary==2.9.9  # PostgreSQL (production)

# Utilities
python-dateutil==2.8.2
pytz==2023.3
```

## Development Workflow

### 1. Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database/init_db.py
```

### 2. Import BPC Data
```bash
python scripts/analyze_products.py  # Analyze first
python scripts/import_bpc_data.py   # Import data
```

### 3. Run Streamlit App
```bash
cd streamlit_app
streamlit run app.py
```

### 4. Development Server
```bash
# FastAPI (if using API endpoints)
uvicorn app.main:app --reload
```

## Authentication with Streamlit

```python
# streamlit_app/services/auth_service.py
import streamlit as st
import streamlit_authenticator as stauth

def check_authentication():
    """Check if user is authenticated."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.switch_page("pages/0_Login.py")
    
    return st.session_state.user
```

## Recommendation Display Example

```python
# streamlit_app/pages/4_🎯_Recommendations.py
import streamlit as st
from services.data_service import get_recommendations

st.title("🎯 Product Recommendations")

recommendations = get_recommendations(st.session_state.org_id)

# Primary ERP Recommendations
st.header("Primary ERP Recommendation")
primary_erps = ['BC', 'D365F', 'D365SCM']
for product_code in primary_erps:
    rec = recommendations.get(product_code)
    if rec:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(rec['name'])
                st.progress(rec['score'] / 100)
            with col2:
                st.metric("Score", f"{rec['score']:.1f}%")
            
            st.write(f"**Recommendation:** {rec['level']}")
            st.write(f"**Coverage:** {rec['must_coverage']:.1f}% of Must requirements")

# CRM Decision
st.header("CRM Analysis")
crm_rec = recommendations.get('CRM')
if crm_rec and crm_rec['score'] > 50:
    st.success(f"✅ CRM Needed - Score: {crm_rec['score']:.1f}%")
    st.write("Customer relationship management capabilities are required.")
else:
    st.info("ℹ️ CRM may not be necessary based on current requirements.")
```

## Next Steps

1. ✅ **Analyze BPC Files** - Run analysis script to identify all products
2. ⏳ **Set up Project Structure** - Create directories
3. ⏳ **Database Setup** - Create SQLite database with schema
4. ⏳ **Excel Parser** - Build parser for BPC files
5. ⏳ **Streamlit App** - Create first page (Process Selection)
6. ⏳ **Recommendation Engine** - Implement scoring algorithm



