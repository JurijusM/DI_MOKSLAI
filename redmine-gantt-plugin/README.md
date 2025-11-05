# Redmine Advanced Gantt Plugin

## ✨ Features Implemented

### Phase 1: SVG Dependencies Visualization ✅

1. **SVG Layer Creation**
   - Dedicated SVG overlay for dependency arrows
   - Proper z-index layering (arrows between grid and bars)
   - Responsive scaling with Gantt chart

2. **Dependency Arrow Rendering**
   - Blue arrows connecting dependent tasks
   - Smooth path rendering with rounded corners
   - Arrowhead markers at the end of each path
   - Automatic path calculation between bars

3. **Junction Point Interactions**
   - Interactive junction points at arrow start/end
   - Hover effect (radius increases from 4px to 6px)
   - Visual feedback with color change on hover

4. **Dependency Context Menu**
   - Right-click on junction points shows menu
   - "View Dependency Details" option
   - "Remove Dependency" option
   - Click outside to close menu

5. **Dependency Management**
   - Remove dependencies via context menu
   - Auto-refresh arrows after changes
   - Notification on successful removal

### Additional Features

1. **Task List Panel**
   - Resizable columns (Name, Duration, Start, Due Date)
   - Fixed row height (56px) for perfect alignment
   - Ellipsis overflow for long task names
   - Hover highlighting synchronized with Gantt bars

2. **Gantt Chart Rendering**
   - Custom HTML/CSS implementation
   - Timeline with months and days
   - Grid lines with weekend highlighting
   - Today marker line

3. **Drag & Drop**
   - Drag entire bar to move task dates
   - Drag left edge to change start date
   - Drag right edge to change due date
   - Visual feedback (dragging/resizing states)
   - Auto-save to backend with notifications

4. **Empty Row Click**
   - Click empty Gantt row to assign default dates
   - Automatically assigns 5 working days from today
   - Skips weekends in calculation

5. **Panel Resizing**
   - Main resizer between task list and Gantt chart
   - Column resizers in task list headers
   - Persistent widths (can be saved to localStorage)

6. **Scroll Synchronization**
   - Vertical scroll sync between panels
   - Prevents scroll loops

## 🚀 Quick Start

### 1. Start Docker Containers

```bash
cd C:\DI_MOKSLAI\redmine-gantt-plugin
docker-compose up -d
```

### 2. Access Redmine

Open browser and go to: http://localhost:3000

Login:
- Username: `admin`
- Password: `admin`

### 3. Access Advanced Gantt

Navigate to: http://localhost:3000/projects/a-gantt/advanced_gantt

## 🎨 SVG Dependencies Features

### How to View Dependencies

Dependencies are automatically rendered as blue arrows between tasks. The arrows:
- Start from the right edge of the predecessor task
- End at the left edge of the successor task
- Include junction points at both ends

### How to Interact with Dependencies

1. **Hover over junction points**: The point will grow larger
2. **Right-click on junction points**: Opens context menu with options:
   - View Dependency Details
   - Remove Dependency

### How Dependencies Update

Dependencies automatically update when:
- Task dates are changed via drag & drop
- Task bars are resized
- Panel widths are adjusted
- Page is refreshed

## 📊 Database Schema

### Dependencies are stored in `issue_relations` table:

```sql
SELECT * FROM issue_relations 
WHERE relation_type = 'precedes';
```

- `issue_from_id`: Predecessor task ID
- `issue_to_id`: Successor task ID
- `relation_type`: 'precedes' (predecessor relationship)
- `delay`: Number of days delay (default 0)

### Example Dependencies in A_GANTT Project:

```
Task 16 → Task 17 (Plugin structure → Register plugin)
Task 17 → Task 18 (Register plugin → Backend API)
Task 18 → Task 19 (Backend API → Frappe Gantt)
Task 20 → Task 21 (i18n → Task list panel)
Task 21 → Task 22 (Task list panel → Text colors)
```

## 🔧 Technical Implementation

### Key Files

1. **JavaScript**: `assets/javascripts/custom_gantt.js`
   - `createSVGLayer()`: Creates SVG container with arrowhead marker
   - `renderDependencies()`: Renders all dependency arrows
   - `drawDependencyArrow()`: Calculates and draws individual arrow
   - `createJunctionPoint()`: Creates interactive circle at arrow ends
   - `showDependencyMenu()`: Shows right-click context menu
   - `removeDependency()`: Removes dependency from map and re-renders

2. **CSS**: `assets/stylesheets/custom_gantt.css`
   - `.dependency-arrow`: Arrow path styling
   - `.dependency-junction`: Junction point styling
   - `.dependency-menu`: Context menu styling

3. **Backend**: `app/controllers/gantt_advanced_controller.rb`
   - `get_dependencies()`: Fetches dependencies from database
   - Returns dependencies array in JSON response

### SVG Implementation Details

```javascript
// SVG Layer Structure
<svg id="gantt-dependencies-svg">
  <defs>
    <marker id="arrowhead">
      <polygon points="0 0, 10 3, 0 6" />
    </marker>
  </defs>
  <!-- Dependency arrows -->
  <path class="dependency-arrow" d="M x1 y1 L ... L x2 y2" />
  <!-- Junction points -->
  <circle class="dependency-junction" cx="x" cy="y" r="4" />
</svg>
```

### Dependency Data Flow

1. **Backend** → Controller fetches issues with relations
2. **Backend** → `get_dependencies()` maps `issue_relations` to dependency IDs
3. **Frontend** → `buildDependenciesMap()` creates Map of dependencies
4. **Frontend** → `renderDependencies()` loops through map
5. **Frontend** → `drawDependencyArrow()` calculates bar positions
6. **Frontend** → SVG path created with `<path>` element
7. **Frontend** → Junction points added as `<circle>` elements

## 🎯 Next Steps (Pending Tasks)

From Redmine Issue #31 subtasks:

### Phase 2: Junction Point Interactions
- ✅ Hover state animation
- ✅ Click to select dependency
- ✅ Visual highlighting

### Phase 3: Dependency Creation Menu
- ⏳ "New dependency" mode activation
- ⏳ Source task selection
- ⏳ Target task selection
- ⏳ Dependency type selector
- ⏳ Save to backend API

### Phase 4: Arrow Path Calculation
- ⏳ Smart routing (avoid overlapping bars)
- ⏳ Curved paths vs straight lines
- ⏳ Multiple dependencies from same task

### Phase 5: Integration & Polish
- ⏳ Dependency validation (no circular dependencies)
- ⏳ Undo/redo support
- ⏳ Keyboard shortcuts
- ⏳ Accessibility (ARIA labels)

## 📝 Logging & Debugging

### Browser Console

Open DevTools (F12) and check console for:
- `🚀 Initializing Custom Gantt with SVG Dependencies`
- `📊 Dependencies map built:`
- `🔗 Rendering dependencies:`
- `✅ Drew arrow: X -> Y`

### Redmine Logs

```bash
docker logs redmine_gantt_app --tail 100 -f
```

## 🐛 Known Issues

1. **Dependencies not showing?**
   - Check if `issue_relations` table has data
   - Verify `relation_type = 'precedes'`
   - Check browser console for errors

2. **Arrows misaligned after resize?**
   - Dependencies auto-refresh after 50ms delay
   - Try manual page refresh if needed

3. **Junction points not clickable?**
   - Check z-index (`pointer-events: all` is set)
   - Verify SVG layer is properly positioned

## 📞 Support

For issues or questions, check:
- Browser DevTools Console (F12)
- Docker logs: `docker logs redmine_gantt_app`
- Redmine production log: `docker exec redmine_gantt_app cat /usr/src/redmine/log/production.log`

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-05  
**Phase 1 Status**: ✅ Complete


