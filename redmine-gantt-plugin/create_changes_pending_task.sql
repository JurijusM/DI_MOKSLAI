-- Create "Changes Pending" feature task in A_GANTT project
\c redmine_development;

DO $$
DECLARE
    v_project_id INTEGER;
    v_tracker_id INTEGER;
    v_status_id INTEGER;
    v_priority_id INTEGER;
    v_author_id INTEGER;
    v_next_issue_id INTEGER;
    v_max_lft INTEGER;
    v_max_rgt INTEGER;
BEGIN
    -- Get project ID
    SELECT id INTO v_project_id FROM projects WHERE identifier = 'a-gantt';
    
    -- Get tracker, status, priority
    SELECT id INTO v_tracker_id FROM trackers WHERE name = 'Feature' LIMIT 1;
    SELECT id INTO v_status_id FROM issue_statuses WHERE name = 'New' LIMIT 1;
    SELECT id INTO v_priority_id FROM enumerations WHERE type = 'IssuePriority' AND name = 'Normal' LIMIT 1;
    SELECT id INTO v_author_id FROM users WHERE login = 'admin' LIMIT 1;
    
    -- Get next issue ID
    SELECT COALESCE(MAX(id), 0) + 1 INTO v_next_issue_id FROM issues;
    
    -- Get max lft and rgt for proper nested set positioning
    SELECT COALESCE(MAX(rgt), 0) INTO v_max_rgt FROM issues WHERE project_id = v_project_id;
    v_max_lft := v_max_rgt + 1;
    v_max_rgt := v_max_lft + 1;
    
    -- Create main task
    INSERT INTO issues (
        id, project_id, tracker_id, subject, description,
        status_id, priority_id, author_id,
        created_on, updated_on,
        lft, rgt
    ) VALUES (
        v_next_issue_id,
        v_project_id,
        v_tracker_id,
        '🔄 "Changes Pending" funkcionalumas - Batch save sistema',
        E'## Problema

**Dabartinė situacija:**
- Visi pakeitimai (drag bar, create dependency) iš karto save\'inasi į backend
- Nėra galimybės peržiūrėti pakeitimų prieš save\'inant
- Nėra galimybės anuliuoti klaidingų pakeitimų
- Sunku daryti kelis pakeitimus ir save\'inti batch\'u

## Siūlomas sprendimas

### **1. "Changes Pending" mygtukas toolbar\'e**
```
[TODAY] [EXPAND ALL] [COLLAPSE ALL] | [⚠️ Changes Pending (5)]
```
- Badge su pakeitimų skaičiumi
- Orange spalva kai yra unsaved changes

### **2. Changes Dialog**
Paspaudus mygtuką → popup su sąrašu pakeitimų:

```
┌─────────────────────────────────────────┐
│  Pending Changes (5)                    │
├─────────────────────────────────────────┤
│ ☑ Task #1: Dates changed                │
│   └ Start: 2025-11-01 → 2025-11-05      │
│   └ Due: 2025-11-15 → 2025-11-20        │
│                                          │
│ ☑ Task #3: Dependency added              │
│   └ Task #3 precedes Task #5            │
│                                          │
│ ☑ Task #7: Dates changed                │
│   └ Start: 2025-12-01 → 2025-12-10      │
│                                          │
│ [ Select All ] [ Deselect All ]         │
│                                          │
│ [Discard Changes] [Save Selected (3)]   │
└─────────────────────────────────────────┘
```

### **3. Workflow:**
1. Darote pakeitimus (drag bars, create dependencies) → tik frontend
2. Mygtukas "Changes Pending" → pasikeičia spalva/badge
3. Click → matote visų pakeitimų sąrašą
4. Pasirenkate kuriuos save\'inti (checkbox\'ai)
5. "Save Selected" → POST į backend tik pasirinktus
6. "Discard Changes" → anuliuoja visus pakeitimus, reload Gantt

## Techninis implementavimas

### **Frontend state management:**
```javascript
let pendingChanges = {
  dateChanges: [
    { issueId: 1, oldStart: \'...\', newStart: \'...\', oldDue: \'...\', newDue: \'...\' }
  ],
  dependencyChanges: [
    { action: \'add\', fromId: 3, toId: 5, type: \'precedes\' },
    { action: \'remove\', fromId: 7, toId: 8, type: \'blocks\' }
  ],
  progressChanges: [
    { issueId: 10, oldProgress: 50, newProgress: 75 }
  ]
};
```

### **Backend batch save endpoint:**
```ruby
POST /projects/:id/advanced_gantt/batch_save
{
  date_changes: [...],
  dependency_changes: [...],
  progress_changes: [...]
}
```

## Pranašumai

1. **Review before save** - matote ką darote
2. **Selective save** - save\'inate tik tai, kas patinka
3. **Undo friendly** - galite discard\'inti klaidas
4. **Performance** - vienas batch API call vietoj 10 atskirų
5. **UX kaip profesionaliose sistemose** (Jira, MS Project)

## Minusai

1. **Sudėtingumas** - reikia state management (~300-500 eilučių kodo)
2. **Conflict handling** - reikia spręsti kas jei kitas user pakeitė tą pačią užduotį
3. **Testing** - daug edge case\'ų

## Estimacija

- **Frontend:** 2-3 valandos
- **Backend:** 1-2 valandos
- **Testing:** 1 valanda
- **Total:** ~4-6 valandos

## Priority

**Low** - nice to have, bet ne blokeris. Dabartinis auto-save veikia, tik nepatogus.',
        v_status_id,
        v_priority_id,
        v_author_id,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        v_max_lft,
        v_max_rgt
    );
    
    RAISE NOTICE '✅ Created task #% - Changes Pending funkcionalumas', v_next_issue_id;
    
END $$;

