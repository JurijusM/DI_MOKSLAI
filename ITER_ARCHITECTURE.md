# ITER - Detailed Architecture Document

## Directory Structure

```
ITER/
├── backend/
│   ├── src/
│   │   ├── config/              # Configuration files
│   │   │   ├── database.ts      # DB connection config
│   │   │   ├── auth.ts          # Auth configuration
│   │   │   └── app.ts           # App configuration
│   │   ├── models/              # Database models/schemas
│   │   │   ├── Organization.ts
│   │   │   ├── User.ts
│   │   │   ├── E2EProcess.ts
│   │   │   ├── BusinessProcess.ts
│   │   │   ├── Scenario.ts
│   │   │   ├── Requirement.ts
│   │   │   └── Recommendation.ts
│   │   ├── controllers/         # Request handlers
│   │   │   ├── auth.controller.ts
│   │   │   ├── process.controller.ts
│   │   │   ├── requirement.controller.ts
│   │   │   ├── dashboard.controller.ts
│   │   │   └── recommendation.controller.ts
│   │   ├── services/            # Business logic
│   │   │   ├── auth.service.ts
│   │   │   ├── process.service.ts
│   │   │   ├── requirement.service.ts
│   │   │   ├── recommendation.service.ts
│   │   │   └── import.service.ts
│   │   ├── middleware/          # Express middleware
│   │   │   ├── auth.middleware.ts
│   │   │   ├── error.middleware.ts
│   │   │   └── validation.middleware.ts
│   │   ├── routes/              # API routes
│   │   │   ├── index.ts
│   │   │   ├── auth.routes.ts
│   │   │   ├── process.routes.ts
│   │   │   ├── requirement.routes.ts
│   │   │   └── dashboard.routes.ts
│   │   ├── utils/               # Utility functions
│   │   │   ├── logger.ts
│   │   │   ├── validators.ts
│   │   │   └── errors.ts
│   │   ├── types/               # TypeScript types
│   │   │   └── index.ts
│   │   └── server.ts            # Entry point
│   ├── migrations/              # Database migrations
│   │   ├── 001_initial_schema.sql
│   │   ├── 002_add_indexes.sql
│   │   └── ...
│   ├── scripts/                 # Utility scripts
│   │   ├── import/
│   │   │   ├── parse-excel.ts
│   │   │   ├── import-processes.ts
│   │   │   └── import-scenarios.ts
│   │   └── seed/                # Seed data
│   │       └── seed-database.ts
│   ├── tests/                   # Backend tests
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   ├── .env.example
│   ├── package.json
│   └── tsconfig.json
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Select.tsx
│   │   │   │   └── LoadingSpinner.tsx
│   │   │   ├── processes/
│   │   │   │   ├── ProcessList.tsx
│   │   │   │   ├── ProcessCard.tsx
│   │   │   │   ├── ProcessFilter.tsx
│   │   │   │   └── PrioritySelector.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── ProgressChart.tsx
│   │   │   │   ├── StatisticsCard.tsx
│   │   │   │   └── CompletionMeter.tsx
│   │   │   └── reports/
│   │   │       ├── FitGapReport.tsx
│   │   │       ├── RecommendationsView.tsx
│   │   │       └── ExportButton.tsx
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── ProcessSelection.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Reports.tsx
│   │   │   └── Admin.tsx
│   │   ├── services/
│   │   │   ├── api.ts           # API client
│   │   │   ├── auth.service.ts
│   │   │   ├── process.service.ts
│   │   │   └── requirement.service.ts
│   │   ├── store/               # State management
│   │   │   ├── slices/
│   │   │   │   ├── auth.slice.ts
│   │   │   │   ├── process.slice.ts
│   │   │   │   └── requirement.slice.ts
│   │   │   └── store.ts
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useProcesses.ts
│   │   │   └── useRequirements.ts
│   │   ├── utils/
│   │   │   ├── constants.ts
│   │   │   ├── formatters.ts
│   │   │   └── validators.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── router.tsx
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
│
├── database/
│   ├── migrations/              # SQL migration files
│   └── seeds/                   # Seed SQL files
│
├── docs/
│   ├── API.md                   # API documentation
│   ├── DEPLOYMENT.md
│   └── USER_GUIDE.md
│
├── .gitignore
├── README.md
└── docker-compose.yml           # For local development
```

## Component Interaction Flow

### Process Selection Flow

```
User → Login → Select E2E Process → View Business Processes 
→ Select Priority (Must/Should/Optional) → Save → Dashboard Update
```

### Recommendation Calculation Flow

```
User Requirements → Identify "Must" Requirements 
→ Match with Scenarios → Calculate Coverage per ERP System 
→ Generate Recommendations → Display with Scores
```

## Database Relationships

```
organizations (1) ──< (many) users
organizations (1) ──< (many) customer_requirements
e2e_processes (1) ──< (many) business_processes
business_processes (1) ──< (many) scenarios
erp_systems (1) ──< (many) scenarios
business_processes (1) ──< (many) customer_requirements
organizations (1) ──< (many) product_recommendations
```

## API Response Examples

### Get Business Processes
```json
GET /api/processes?e2e_process=order-to-cash

Response:
{
  "data": [
    {
      "id": "uuid",
      "processCode": "65.05.040",
      "name": "Develop sales catalogs",
      "description": "...",
      "e2eProcess": {
        "code": "order-to-cash",
        "name": "Order to Cash"
      },
      "userRequirement": {
        "priority": "must",
        "updatedAt": "2025-01-15T10:30:00Z"
      }
    }
  ],
  "total": 45,
  "page": 1,
  "pageSize": 20
}
```

### Update Requirement
```json
PUT /api/requirements/123

Request:
{
  "businessProcessId": "uuid",
  "priority": "must",
  "notes": "Critical for Q2 launch"
}

Response:
{
  "data": {
    "id": "uuid",
    "priority": "must",
    "updatedAt": "2025-01-15T10:35:00Z",
    "selectedBy": {
      "id": "user-uuid",
      "name": "John Doe"
    }
  }
}
```

### Get Recommendations
```json
GET /api/recommendations

Response:
{
  "data": [
    {
      "erpSystem": {
        "code": "BC",
        "name": "Business Central"
      },
      "score": 87.5,
      "coverage": 85.0,
      "mustRequirementsCovered": 34,
      "totalMustRequirements": 40,
      "recommendation": "Highly Recommended",
      "strengths": [
        "Covers all sales catalog requirements",
        "Strong order management capabilities"
      ],
      "gaps": [
        "Limited advanced analytics",
        "No built-in CRM integration"
      ]
    }
  ]
}
```

## Security Architecture

### Authentication Flow
1. User logs in → JWT access token + refresh token issued
2. Access token (15 min expiry) used for API calls
3. Refresh token (7 days expiry) stored in httpOnly cookie
4. Token refresh mechanism before expiry

### Authorization Levels
- **Admin**: Full access, can manage organizations and users
- **Consultant**: Can view all organizations, manage requirements
- **Customer**: Can only manage own organization's requirements

### Multi-Tenant Isolation
- All queries filtered by `organization_id`
- Row-level security policies in database
- Middleware validates organization access

## Performance Considerations

1. **Caching Strategy**:
   - Redis for frequently accessed process data
   - Frontend caching for process lists (stale-while-revalidate)

2. **Database Optimization**:
   - Indexed columns for frequent queries
   - Materialized views for recommendation calculations
   - Partitioning for large requirement history tables

3. **Frontend Optimization**:
   - Lazy loading for process lists
   - Virtual scrolling for long lists
   - Code splitting for routes

## Error Handling

### Standard Error Response Format
```json
{
  "error": {
    "code": "PROCESS_NOT_FOUND",
    "message": "Business process not found",
    "details": {},
    "timestamp": "2025-01-15T10:40:00Z"
  }
}
```

### Error Categories
- **400**: Bad Request (validation errors)
- **401**: Unauthorized (authentication required)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found
- **500**: Internal Server Error

## Testing Strategy

### Unit Tests
- Services: Business logic validation
- Controllers: Request/response handling
- Components: UI rendering and interactions

### Integration Tests
- API endpoints: Full request/response cycle
- Database operations: CRUD operations
- Authentication flow

### E2E Tests
- Complete user workflows
- Cross-browser testing
- Performance testing

## Deployment Architecture

### Development
- SQLite database (local)
- Node.js dev server
- React dev server (Vite/CRA)

### Staging
- PostgreSQL (containerized)
- Backend on Azure App Service
- Frontend on Azure Static Web Apps

### Production
- Azure SQL Database or Azure Database for PostgreSQL
- Azure App Service (Backend)
- Azure Static Web Apps (Frontend)
- Azure Active Directory for authentication
- Application Insights for monitoring

## Monitoring & Logging

1. **Application Logs**: Winston/Pino for structured logging
2. **Error Tracking**: Sentry or Application Insights
3. **Performance Monitoring**: Application Insights
4. **User Analytics**: Track feature usage and completion rates

## Data Import Process

### Excel Parsing Strategy
1. Read all BPC Excel files from directory
2. Identify sheets/tabs (E2E processes)
3. Extract process codes and names
4. Extract scenarios with system mappings
5. Validate data consistency
6. Bulk insert into database with transaction
7. Generate import report

### Import Script Workflow
```typescript
// Pseudo-code
async function importBPCFiles(directory: string) {
  const files = await readDirectory(directory);
  
  for (const file of files) {
    const workbook = await parseExcel(file);
    
    for (const sheet of workbook.sheets) {
      const e2eProcess = extractE2EProcess(sheet);
      const processes = extractBusinessProcesses(sheet);
      
      for (const process of processes) {
        const scenarios = extractScenarios(process);
        await saveProcessWithScenarios(process, scenarios);
      }
    }
  }
}
```



