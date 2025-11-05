# ITER - Intelligent Technology Evaluation & Requirements
## Self-Service ERP Requirements Gathering Platform

### Project Overview

**Purpose**: Accelerate ERP requirements gathering and product selection through a self-service portal that enables key users to prioritize business processes and scenarios, identifying fit/gap analysis between customer needs and Microsoft ERP solutions (Business Central, D365 Finance, D365 Supply Chain, CRM, etc.).

**Target Users**: 
- Internal consultants and analysts (intranet)
- External customers (extranet)

**Core Value Proposition**: Reduce requirements gathering time by 60-70% through guided, structured process evaluation.

---

## 1. Requirements Analysis

### 1.1 Data Structure Understanding
Based on Microsoft Business Process Catalog (BPC) files:
- **End-to-End Processes**: Order to Cash, Acquire to Dispose, Source to Pay, etc.
- **Process Code Format**: `65.05.040` (Develop sales catalogs)
- **Scenario Format**: `65.05.040.100` (System-specific implementations)
  - `.100` = Dynamics 365 Supply Chain Management
  - `.101` = Dynamics 365 Business Central
  - Additional codes for other systems (CRM, Finance, etc.)

### 1.2 Key Requirements
1. **Process Display**: Show process names without system-specific scenario IDs
2. **Priority Selection**: Must / Should / Optional per process
3. **Progress Tracking**: Dashboard showing completion status
4. **Authentication**: Track who made decisions and when
5. **Reporting**: Generate fit/gap analysis reports
6. **Multi-tenant**: Support multiple customer organizations

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Streamlit Frontend (Python)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Process     │  │  Dashboard   │  │  Reports    │       │
│  │  Selection   │  │   & Progress │  │   & Export  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            │
                    ┌───────┴───────┐
                    │  FastAPI      │
                    │  (Python)     │
                    │  (Optional)  │
                    └───────┬───────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
    ┌───────▼────┐  ┌──────▼────┐  ┌──────▼────┐
    │  Auth      │  │  Business │  │  Data     │
    │  Service   │  │  Logic    │  │  Access   │
    │            │  │  Layer    │  │  Layer    │
    └────────────┘  └───────────┘  └───────────┘
                            │
                    ┌───────▼───────┐
                    │   Database    │
                    │  (SQLite/     │
                    │   PostgreSQL) │
                    └───────────────┘
```

### 2.2 Technology Stack Decision ✅

**Frontend:**
- **Framework**: Streamlit (Python-based UI)
  - Fast development - UI built with Python
  - Perfect for internal tools and self-service portals
  - Built-in widgets for forms, charts, and dashboards
  - Easy authentication integration
  - Multi-page app support

**Backend:**
- **Runtime**: Python 3.11+ with FastAPI (optional for API endpoints)
- **Language**: Python 3.11+
- **Validation**: Pydantic for data validation
- **ORM**: SQLAlchemy for database access

**Database:**
- **Primary**: PostgreSQL (recommended over SQLite for production)
  - Better concurrent user support
  - Advanced features (JSON columns, full-text search)
  - Better for multi-tenant architecture
- **Alternative**: SQL Server (if already in Microsoft ecosystem)

**Authentication:**
- **Option 1**: Microsoft Entra ID (Azure AD) for SSO
- **Option 2**: JWT-based authentication with refresh tokens
- **Option 3**: OAuth 2.0 / OpenID Connect

**File Processing:**
- **Excel Parser**: `openpyxl` and `pandas` (Python) to import BPC data

**Hosting:**
- **Streamlit App**: Streamlit Cloud, Azure Container Instances, or Docker
- **Database**: SQLite for development, PostgreSQL for production
- **Alternative**: Azure App Service with Python runtime

**Key Python Packages:**
- `streamlit` - UI framework
- `fastapi` - API framework (optional)
- `sqlalchemy` - ORM
- `pandas` + `openpyxl` - Excel processing
- `plotly` - Interactive charts
- `python-jose` - JWT authentication

---

## 3. Database Schema Design

### 3.1 Core Tables

```sql
-- Organizations (Multi-tenant support)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user', -- 'admin', 'consultant', 'customer'
    auth_provider VARCHAR(50), -- 'azure_ad', 'local', 'oauth'
    external_id VARCHAR(255), -- ID from auth provider
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- End-to-End Processes (from BPC files)
CREATE TABLE e2e_processes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL, -- e.g., "Order to Cash"
    name VARCHAR(255) NOT NULL,
    description TEXT,
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Business Processes (e.g., "65.05.040 Develop sales catalogs")
CREATE TABLE business_processes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    process_code VARCHAR(50) UNIQUE NOT NULL, -- "65.05.040"
    name VARCHAR(255) NOT NULL, -- "Develop sales catalogs"
    description TEXT,
    e2e_process_id UUID REFERENCES e2e_processes(id),
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ERP Systems
CREATE TABLE erp_systems (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL, -- "BC", "D365F", "D365SCM", "CRM"
    name VARCHAR(255) NOT NULL, -- "Business Central", "D365 Finance"
    description TEXT,
    display_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scenarios (System-specific implementations)
CREATE TABLE scenarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scenario_code VARCHAR(50) NOT NULL, -- "65.05.040.100"
    business_process_id UUID REFERENCES business_processes(id),
    erp_system_id UUID REFERENCES erp_systems(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    sequence_number INTEGER, -- 100, 101, etc. (to map back to .100, .101)
    UNIQUE(scenario_code, erp_system_id)
);

-- Customer Requirements (User selections)
CREATE TABLE customer_requirements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    business_process_id UUID REFERENCES business_processes(id),
    priority VARCHAR(20) NOT NULL, -- 'must', 'should', 'optional', 'not_needed'
    notes TEXT,
    selected_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, business_process_id)
);

-- Requirement History (Audit trail)
CREATE TABLE requirement_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    requirement_id UUID REFERENCES customer_requirements(id),
    previous_priority VARCHAR(20),
    new_priority VARCHAR(20),
    changed_by UUID REFERENCES users(id),
    change_reason TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product Recommendations (System-generated)
CREATE TABLE product_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    erp_system_id UUID REFERENCES erp_systems(id),
    recommendation_score DECIMAL(5,2), -- 0-100
    coverage_percentage DECIMAL(5,2), -- % of "must" requirements covered
    recommendation_reason TEXT,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2 Indexes

```sql
CREATE INDEX idx_customer_requirements_org ON customer_requirements(organization_id);
CREATE INDEX idx_customer_requirements_process ON customer_requirements(business_process_id);
CREATE INDEX idx_scenarios_process ON scenarios(business_process_id);
CREATE INDEX idx_scenarios_system ON scenarios(erp_system_id);
CREATE INDEX idx_users_org ON users(organization_id);
```

---

## 4. API Structure

### 4.1 RESTful API Endpoints

**Authentication:**
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

**Processes:**
- `GET /api/processes/e2e` - Get all end-to-end processes
- `GET /api/processes` - Get business processes (filtered by e2e_process)
- `GET /api/processes/:processCode` - Get specific process details

**Requirements:**
- `GET /api/requirements` - Get organization's requirements
- `POST /api/requirements` - Create/update requirement
- `PUT /api/requirements/:id` - Update requirement priority
- `GET /api/requirements/summary` - Get summary statistics

**Dashboard:**
- `GET /api/dashboard/progress` - Get completion progress
- `GET /api/dashboard/statistics` - Get requirement statistics

**Recommendations:**
- `GET /api/recommendations` - Get ERP product recommendations
- `POST /api/recommendations/calculate` - Recalculate recommendations

**Reports:**
- `GET /api/reports/fit-gap` - Generate fit/gap analysis
- `GET /api/reports/export` - Export requirements to Excel/PDF

**Admin:**
- `POST /api/admin/import-bpc` - Import BPC Excel files
- `GET /api/admin/organizations` - Manage organizations
- `GET /api/admin/users` - Manage users

---

## 5. Streamlit App Structure

```
streamlit_app/
├── pages/
│   ├── 1_🏠_Home.py                 # Welcome & overview
│   ├── 2_📋_Process_Selection.py    # Main feature - select priorities
│   ├── 3_📊_Dashboard.py            # Progress tracking
│   ├── 4_🎯_Recommendations.py      # Product recommendations
│   └── 5_📄_Reports.py               # Export & fit/gap analysis
├── components/
│   ├── process_card.py              # Process display card
│   ├── priority_selector.py         # Must/Should/Optional selector
│   ├── progress_chart.py            # Progress visualization
│   └── recommendation_card.py       # Product recommendation display
├── services/
│   ├── auth_service.py              # Authentication
│   └── data_service.py              # Database access
├── utils/
│   └── session_state.py             # Streamlit session management
├── .streamlit/
│   └── config.toml                  # Streamlit configuration
└── app.py                           # Main entry point
```

---

## 6. Development Phases

### Phase 1: Foundation (Weeks 1-2)
- [ ] Set up project structure (frontend + backend)
- [ ] Database schema creation and migration scripts
- [ ] Basic authentication implementation
- [ ] Excel parser for BPC data import
- [ ] Initial data import from BPC files

### Phase 2: Core Features (Weeks 3-4)
- [ ] Process listing and filtering UI
- [ ] Priority selection (Must/Should/Optional)
- [ ] API endpoints for requirements CRUD
- [ ] Database persistence
- [ ] Basic dashboard showing progress

### Phase 3: Dashboard & Reports (Week 5)
- [ ] Advanced dashboard with statistics
- [ ] Progress tracking visualization
- [ ] Requirement summary reports
- [ ] Export functionality (Excel/PDF)

### Phase 4: Recommendations Engine (Week 6)
- [ ] Algorithm for product recommendation
- [ ] Coverage calculation (how well each ERP covers "must" requirements)
- [ ] Recommendation display and comparison

### Phase 5: Polish & Security (Week 7)
- [ ] Multi-tenant isolation
- [ ] Audit logging
- [ ] Role-based access control
- [ ] UI/UX improvements
- [ ] Error handling and validation

### Phase 6: Testing & Deployment (Week 8)
- [ ] Unit tests
- [ ] Integration tests
- [ ] User acceptance testing
- [ ] Production deployment
- [ ] Documentation

---

## 7. Key Design Decisions

### 7.1 Process Display Logic
- Users see: "Develop sales catalogs" (from `business_processes.name`)
- System internally maps to scenarios: `.100`, `.101`, etc.
- Recommendation engine evaluates which ERP systems can fulfill the requirement

### 7.2 Priority Levels
- **Must**: Critical requirement, cannot proceed without
- **Should**: Important but not critical
- **Optional**: Nice to have
- **Not Needed**: Explicitly excluded

### 7.3 Recommendation Algorithm & Product Mapping

**Microsoft Products Supported:**
- **Primary ERP**: Business Central (BC), D365 Finance (D365F), D365 Supply Chain (D365SCM), D365 Commerce (D365COMM)
- **CRM**: D365 Sales (CRM), D365 Customer Service (D365CS), D365 Field Service (D365FS)
- **Specialized**: D365 Project Operations (D365PO), D365 Human Resources (D365HR)

**Scoring Algorithm:**
1. **Requirement Analysis**: 
   - Identify all "must" requirements (70% weight)
   - Identify all "should" requirements (25% weight)
   - Identify all "optional" requirements (5% weight)

2. **Product Coverage Calculation**:
   - For each Microsoft product, find scenarios that map to user requirements
   - Calculate coverage: (Covered Requirements / Total Requirements) × 100
   - Example: If user has 40 "must" requirements and BC covers 34, coverage = 85%

3. **Score Calculation**:
   - Must Score = (Must Coverage × 0.7)
   - Should Score = (Should Coverage × 0.25)
   - Optional Score = (Optional Coverage × 0.05)
   - **Total Score = Must + Should + Optional**

4. **Recommendation Generation**:
   - **Primary ERP**: Compare BC vs D365F vs D365SCM vs D365COMM → Highest score wins
   - **CRM Decision**: If CRM product score ≥ 50% → CRM needed
   - **Additional Products**: Recommend specialized products if score ≥ 50%

5. **Output After Discovery**:
   - Primary ERP recommendation with score
   - CRM needed (Yes/No) with score
   - Additional products list
   - Gap analysis (missing "must" requirements)

**Example Output:**
```
Primary Recommendation: Dynamics 365 Business Central (Score: 87%)
  - Covers 85% of "Must Have" requirements
  - 5 critical gaps identified

CRM Needed: Yes - Dynamics 365 Sales (Score: 78%)
  - Customer management capabilities required

Additional Products:
  - Dynamics 365 Commerce (Score: 65%) - Recommended for e-commerce
```

### 7.4 Multi-Tenancy
- Organization-based isolation at database level
- Users belong to one organization
- Requirements are organization-scoped

---

## 8. Security Considerations

1. **Authentication**: 
   - JWT tokens with short expiration
   - Refresh token rotation
   - Secure password storage (if local auth)

2. **Authorization**:
   - Organization-level access control
   - Role-based permissions (admin, consultant, customer)

3. **Data Privacy**:
   - Audit trail for all requirement changes
   - GDPR compliance considerations
   - Data export capabilities

4. **API Security**:
   - Rate limiting
   - Input validation
   - SQL injection prevention
   - CORS configuration

---

## 9. File Import Strategy

### 9.1 BPC Excel File Processing
1. Parse Excel files from `C:\DI_MOKSLAI\GO_FAST\`
2. Extract:
   - End-to-end process names (sheet names or headers)
   - Process codes (e.g., "65.05.040")
   - Process names (e.g., "Develop sales catalogs")
   - Scenarios with system mappings (.100, .101, etc.)
3. Import into database with validation
4. Support re-import with update logic

### 9.2 Import Script Structure
```
scripts/
├── import/
│   ├── parse-bpc-excel.js    # Excel parser
│   ├── import-processes.js    # Import business processes
│   ├── import-scenarios.js    # Import scenarios
│   └── validate-data.js       # Data validation
```

---

## 10. Next Steps

1. **Confirm Technology Stack**: Review and approve recommended stack
2. **Data Extraction**: Create script to parse existing BPC Excel files
3. **Proof of Concept**: Build minimal viable version with one E2E process
4. **Stakeholder Review**: Present architecture to stakeholders
5. **Development Start**: Begin Phase 1 development

---

## Appendix A: Alternative Database Option

**SQLite** can be used for:
- Development/Testing
- Single-tenant deployments
- Small teams (< 10 concurrent users)

**PostgreSQL recommended for**:
- Production multi-tenant
- Concurrent users (50+)
- Future scalability

We can start with SQLite and migrate to PostgreSQL when needed.

---

## Appendix B: Reference - Seer Product Guide 365

Seer Product Guide 365 (or similar Microsoft guidance tools) provide:
- Interactive decision trees
- Scenario-based recommendations
- Visual progress tracking
- Comparison matrices

ITER will incorporate these UX patterns while focusing on the pre-implementation requirements gathering phase.

