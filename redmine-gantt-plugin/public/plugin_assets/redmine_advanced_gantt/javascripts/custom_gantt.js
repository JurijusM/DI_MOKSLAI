// Custom Gantt Chart with SVG Dependencies
let ganttData = [];
let projectId = null;
let dateRange = null;
let dayWidth = 40;
let dependenciesMap = new Map();

function initializeCustomGantt(pId, data) {
  console.log('🚀 Initializing Custom Gantt with SVG Dependencies');
  projectId = pId;
  ganttData = data;
  
  // Build dependencies map
  buildDependenciesMap();
  
  // Calculate date range
  dateRange = calculateDateRange(ganttData);
  
  if (!dateRange) {
    showError('No valid date range found');
    return;
  }
  
  // Render components
  renderCustomGantt();
  renderTaskList();
  
  // Setup interactions
  setupEventListeners();
  setupResizer();
  setupColumnResizers();
  setupScrollSync();
  setupGanttBarInteractions();
  
  console.log('✅ Custom Gantt initialized successfully');
}

function buildDependenciesMap() {
  dependenciesMap.clear();
  ganttData.forEach(task => {
    if (task.dependencies && task.dependencies.length > 0) {
      task.dependencies.forEach(depId => {
        if (!dependenciesMap.has(task.id)) {
          dependenciesMap.set(task.id, []);
        }
        dependenciesMap.get(task.id).push(depId);
      });
    }
  });
  console.log('📊 Dependencies map built:', dependenciesMap);
}

function calculateDateRange(tasks) {
  let minDate = null;
  let maxDate = null;
  
  tasks.forEach(task => {
    if (task.start && task.end) {
      const start = new Date(task.start);
      const end = new Date(task.end);
      
      if (!minDate || start < minDate) minDate = start;
      if (!maxDate || end > maxDate) maxDate = end;
    }
  });
  
  if (!minDate || !maxDate) {
    const today = new Date();
    minDate = new Date(today);
    minDate.setMonth(today.getMonth() - 1);
    maxDate = new Date(today);
    maxDate.setMonth(today.getMonth() + 2);
  }
  
  // Add padding
  minDate.setDate(minDate.getDate() - 7);
  maxDate.setDate(maxDate.getDate() + 7);
  
  return { start: minDate, end: maxDate };
}

function renderCustomGantt() {
  const container = document.getElementById('gantt-container');
  if (!container) {
    console.error('❌ Gantt container not found');
    return;
  }
  
  const wrapper = document.createElement('div');
  wrapper.className = 'custom-gantt-wrapper';
  wrapper.id = 'custom-gantt-wrapper';
  
  // Timeline
  const timeline = renderTimeline();
  wrapper.appendChild(timeline);
  
  // Gantt rows with grid lines
  const rowsContainer = document.createElement('div');
  rowsContainer.className = 'custom-gantt-rows';
  rowsContainer.id = 'custom-gantt-rows';
  
  // Add grid lines
  const gridLines = renderGridLines();
  rowsContainer.appendChild(gridLines);
  
  // Add task rows and bars
  ganttData.forEach((task, index) => {
    const row = renderGanttRow(task, index);
    rowsContainer.appendChild(row);
  });
  
  wrapper.appendChild(rowsContainer);
  
  // SVG Dependencies Layer
  const svgLayer = createSVGLayer();
  rowsContainer.appendChild(svgLayer);
  
  container.innerHTML = '';
  container.appendChild(wrapper);
  
  // Render dependencies after DOM is ready
  setTimeout(() => renderDependencies(), 100);
}

function renderTimeline() {
  const timeline = document.createElement('div');
  timeline.className = 'custom-gantt-timeline';
  
  // Months row
  const monthsRow = document.createElement('div');
  monthsRow.className = 'timeline-months';
  
  const months = getMonthsInRange(dateRange.start, dateRange.end);
  months.forEach(month => {
    const monthDiv = document.createElement('div');
    monthDiv.className = 'timeline-month';
    monthDiv.style.width = `${month.days * dayWidth}px`;
    monthDiv.textContent = month.label;
    monthsRow.appendChild(monthDiv);
  });
  
  timeline.appendChild(monthsRow);
  
  // Days row
  const daysRow = document.createElement('div');
  daysRow.className = 'timeline-days';
  
  const totalDays = Math.ceil((dateRange.end - dateRange.start) / (1000 * 60 * 60 * 24));
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  for (let i = 0; i < totalDays; i++) {
    const date = new Date(dateRange.start);
    date.setDate(date.getDate() + i);
    
    const dayDiv = document.createElement('div');
    dayDiv.className = 'timeline-day';
    dayDiv.style.width = `${dayWidth}px`;
    
    const dayOfWeek = date.getDay();
    if (dayOfWeek === 0 || dayOfWeek === 6) {
      dayDiv.classList.add('weekend');
    }
    
    if (date.getTime() === today.getTime()) {
      dayDiv.classList.add('today');
    }
    
    dayDiv.textContent = date.getDate();
    dayDiv.setAttribute('data-date', date.toISOString().split('T')[0]);
    daysRow.appendChild(dayDiv);
  }
  
  timeline.appendChild(daysRow);
  
  return timeline;
}

function renderGridLines() {
  const gridContainer = document.createElement('div');
  gridContainer.className = 'gantt-grid-lines';
  
  const totalDays = Math.ceil((dateRange.end - dateRange.start) / (1000 * 60 * 60 * 24));
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  for (let i = 0; i < totalDays; i++) {
    const date = new Date(dateRange.start);
    date.setDate(date.getDate() + i);
    
    const line = document.createElement('div');
    line.className = 'gantt-grid-line';
    line.style.left = `${i * dayWidth}px`;
    
    const dayOfWeek = date.getDay();
    if (dayOfWeek === 0 || dayOfWeek === 6) {
      line.classList.add('weekend');
    }
    
    if (date.getTime() === today.getTime()) {
      line.classList.add('today');
    }
    
    gridContainer.appendChild(line);
  }
  
  return gridContainer;
}

function renderGanttRow(task, index) {
  const row = document.createElement('div');
  row.className = 'custom-gantt-row';
  row.id = `gantt-row-${task.id}`;
  row.setAttribute('data-task-id', task.id);
  
  if (task.start && task.end) {
    const bar = createGanttBar(task);
    row.appendChild(bar);
  } else {
    // Empty row hint
    const hint = document.createElement('div');
    hint.className = 'gantt-empty-row-hint';
    hint.textContent = 'Click to assign dates';
    row.appendChild(hint);
    
    // Click handler for empty rows
    row.addEventListener('click', (e) => {
      if (e.target === row || e.target.classList.contains('gantt-empty-row-hint')) {
        assignDefaultDates(task.id);
      }
    });
  }
  
  return row;
}

function createGanttBar(task) {
  const startDate = new Date(task.start);
  const endDate = new Date(task.end);
  
  const startOffset = Math.floor((startDate - dateRange.start) / (1000 * 60 * 60 * 24));
  const duration = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
  
  const bar = document.createElement('div');
  bar.className = `gantt-bar ${task.status_class || 'gantt-new'}`;
  bar.id = `gantt-bar-${task.id}`;
  bar.setAttribute('data-task-id', task.id);
  bar.style.left = `${startOffset * dayWidth}px`;
  bar.style.width = `${duration * dayWidth}px`;
  
  // Progress bar
  if (task.progress > 0) {
    const progressBar = document.createElement('div');
    progressBar.className = 'gantt-bar-progress';
    progressBar.style.width = `${task.progress}%`;
    bar.appendChild(progressBar);
  }
  
  // Label
  const label = document.createElement('div');
  label.className = 'gantt-bar-label';
  label.textContent = task.name;
  bar.appendChild(label);
  
  // Add junction points for dependency creation
  const startJunction = document.createElement('div');
  startJunction.className = 'junction-point start';
  startJunction.setAttribute('data-junction-type', 'start');
  startJunction.setAttribute('data-task-id', task.id);
  startJunction.title = `${task.name} (start)`;
  
  const endJunction = document.createElement('div');
  endJunction.className = 'junction-point end';
  endJunction.setAttribute('data-junction-type', 'end');
  endJunction.setAttribute('data-task-id', task.id);
  endJunction.title = `${task.name} (end)`;
  
  bar.appendChild(startJunction);
  bar.appendChild(endJunction);
  
  return bar;
}

// SVG Dependencies Layer
function createSVGLayer() {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.id = 'gantt-dependencies-svg';
  svg.setAttribute('width', '100%');
  svg.setAttribute('height', '100%');
  
  // Define arrowhead marker
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
  marker.setAttribute('id', 'arrowhead');
  marker.setAttribute('markerWidth', '10');
  marker.setAttribute('markerHeight', '10');
  marker.setAttribute('refX', '9');
  marker.setAttribute('refY', '3');
  marker.setAttribute('orient', 'auto');
  
  const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
  polygon.setAttribute('points', '0 0, 10 3, 0 6');
  polygon.setAttribute('fill', '#2196F3');
  
  marker.appendChild(polygon);
  defs.appendChild(marker);
  svg.appendChild(defs);
  
  return svg;
}

function renderDependencies() {
  const svg = document.getElementById('gantt-dependencies-svg');
  if (!svg) {
    console.warn('⚠️ SVG layer not found');
    return;
  }
  
  // Clear existing dependencies
  while (svg.childNodes.length > 1) { // Keep defs
    svg.removeChild(svg.lastChild);
  }
  
  console.log('🔗 Rendering dependencies:', dependenciesMap);
  
  dependenciesMap.forEach((dependencies, fromTaskId) => {
    dependencies.forEach(toTaskId => {
      drawDependencyArrow(fromTaskId, toTaskId, svg);
    });
  });
}

function drawDependencyArrow(fromTaskId, toTaskId, svg) {
  const fromBar = document.getElementById(`gantt-bar-${fromTaskId}`);
  const toBar = document.getElementById(`gantt-bar-${toTaskId}`);
  
  if (!fromBar || !toBar) {
    console.warn(`⚠️ Bars not found for dependency: ${fromTaskId} -> ${toTaskId}`);
    return;
  }
  
  const fromRect = fromBar.getBoundingClientRect();
  const toRect = toBar.getBoundingClientRect();
  const svgRect = svg.getBoundingClientRect();
  
  // Calculate positions relative to SVG
  const fromX = fromRect.right - svgRect.left;
  const fromY = fromRect.top + fromRect.height / 2 - svgRect.top;
  const toX = toRect.left - svgRect.left;
  const toY = toRect.top + toRect.height / 2 - svgRect.top;
  
  // Create path with rounded corners
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  
  const midX = (fromX + toX) / 2;
  const pathData = `M ${fromX} ${fromY} L ${midX} ${fromY} L ${midX} ${toY} L ${toX} ${toY}`;
  
  path.setAttribute('d', pathData);
  path.setAttribute('class', 'dependency-arrow');
  path.setAttribute('data-from', fromTaskId);
  path.setAttribute('data-to', toTaskId);
  
  // Add junction points
  const junctionFrom = createJunctionPoint(fromX, fromY, fromTaskId, toTaskId, 'from');
  const junctionTo = createJunctionPoint(toX, toY, fromTaskId, toTaskId, 'to');
  
  svg.appendChild(path);
  svg.appendChild(junctionFrom);
  svg.appendChild(junctionTo);
  
  console.log(`✅ Drew arrow: ${fromTaskId} -> ${toTaskId}`);
}

function createJunctionPoint(x, y, fromTaskId, toTaskId, type) {
  const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  circle.setAttribute('cx', x);
  circle.setAttribute('cy', y);
  circle.setAttribute('r', '4');
  circle.setAttribute('class', 'dependency-junction');
  circle.setAttribute('data-from', fromTaskId);
  circle.setAttribute('data-to', toTaskId);
  circle.setAttribute('data-type', type);
  
  // Hover effect
  circle.addEventListener('mouseenter', () => {
    circle.setAttribute('r', '6');
  });
  
  circle.addEventListener('mouseleave', () => {
    circle.setAttribute('r', '4');
  });
  
  // Right-click menu
  circle.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    showDependencyMenu(e, fromTaskId, toTaskId);
  });
  
  return circle;
}

function showDependencyMenu(event, fromTaskId, toTaskId) {
  // Remove existing menu
  const existingMenu = document.querySelector('.dependency-menu');
  if (existingMenu) {
    existingMenu.remove();
  }
  
  const menu = document.createElement('div');
  menu.className = 'dependency-menu';
  menu.style.left = `${event.pageX}px`;
  menu.style.top = `${event.pageY}px`;
  
  const viewItem = document.createElement('div');
  viewItem.className = 'dependency-menu-item';
  viewItem.textContent = 'View Dependency Details';
  viewItem.addEventListener('click', () => {
    console.log(`Dependency: ${fromTaskId} -> ${toTaskId}`);
    menu.remove();
  });
  
  const removeItem = document.createElement('div');
  removeItem.className = 'dependency-menu-item';
  removeItem.textContent = 'Remove Dependency';
  removeItem.addEventListener('click', () => {
    removeDependency(fromTaskId, toTaskId);
    menu.remove();
  });
  
  menu.appendChild(viewItem);
  menu.appendChild(document.createElement('div')).className = 'dependency-menu-divider';
  menu.appendChild(removeItem);
  
  document.body.appendChild(menu);
  
  // Close menu on click outside
  setTimeout(() => {
    document.addEventListener('click', function closeMenu() {
      menu.remove();
      document.removeEventListener('click', closeMenu);
    });
  }, 10);
}

function removeDependency(fromTaskId, toTaskId) {
  const deps = dependenciesMap.get(fromTaskId);
  if (deps) {
    const index = deps.indexOf(toTaskId);
    if (index > -1) {
      deps.splice(index, 1);
      if (deps.length === 0) {
        dependenciesMap.delete(fromTaskId);
      }
      renderDependencies();
      showNotification('Dependency removed successfully', 'success');
    }
  }
}

function renderTaskList() {
  const taskListBody = document.getElementById('task-list-body');
  if (!taskListBody) {
    console.error('❌ Task list body not found');
    return;
  }
  
  const table = document.createElement('table');
  table.className = 'task-list-table';
  
  const tbody = document.createElement('tbody');
  
  ganttData.forEach(task => {
    const row = document.createElement('tr');
    row.id = `task-row-${task.id}`;
    row.setAttribute('data-task-id', task.id);
    
    // Name
    const nameCell = document.createElement('td');
    nameCell.className = 'task-name-cell';
    
    const nameSpan = document.createElement('span');
    nameSpan.className = 'task-name';
    nameSpan.textContent = task.name;
    
    // External link icon
    const linkIcon = document.createElement('a');
    linkIcon.className = 'task-external-link';
    linkIcon.href = `/issues/${task.id}`;
    linkIcon.target = '_blank';
    linkIcon.title = 'Open in new tab';
    linkIcon.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>';
    linkIcon.onclick = (e) => e.stopPropagation(); // Prevent row click
    
    nameCell.appendChild(nameSpan);
    nameCell.appendChild(linkIcon);
    row.appendChild(nameCell);
    
    // Duration
    const durationCell = document.createElement('td');
    durationCell.className = 'task-duration-cell';
    durationCell.textContent = calculateDuration(task);
    row.appendChild(durationCell);
    
    // Start date
    const startCell = document.createElement('td');
    startCell.className = 'task-date-cell task-start-cell';
    startCell.textContent = task.start ? formatDate(new Date(task.start)) : '-';
    row.appendChild(startCell);
    
    // Due date
    const dueCell = document.createElement('td');
    dueCell.className = 'task-date-cell task-due-cell';
    dueCell.textContent = task.end ? formatDate(new Date(task.end)) : '-';
    row.appendChild(dueCell);
    
    // Hover effect
    row.addEventListener('mouseenter', () => {
      highlightGanttRow(task.id);
    });
    
    row.addEventListener('mouseleave', () => {
      removeGanttRowHighlight(task.id);
    });
    
    tbody.appendChild(row);
  });
  
  table.appendChild(tbody);
  taskListBody.innerHTML = '';
  taskListBody.appendChild(table);
}

function calculateDuration(task) {
  if (!task.start || !task.end) return '-';
  
  const start = new Date(task.start);
  const end = new Date(task.end);
  const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
  
  return `${days}d`;
}

function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function highlightGanttRow(taskId) {
  const ganttRow = document.getElementById(`gantt-row-${taskId}`);
  const taskRow = document.getElementById(`task-row-${taskId}`);
  const ganttBar = document.getElementById(`gantt-bar-${taskId}`);
  
  if (ganttRow) ganttRow.classList.add('highlighted');
  if (taskRow) taskRow.classList.add('highlighted');
  if (ganttBar) ganttBar.style.transform = 'translateY(-1px)';
}

function removeGanttRowHighlight(taskId) {
  const ganttRow = document.getElementById(`gantt-row-${taskId}`);
  const taskRow = document.getElementById(`task-row-${taskId}`);
  const ganttBar = document.getElementById(`gantt-bar-${taskId}`);
  
  if (ganttRow) ganttRow.classList.remove('highlighted');
  if (taskRow) taskRow.classList.remove('highlighted');
  if (ganttBar) ganttBar.style.transform = '';
}

// Assign default dates (5 working days)
function assignDefaultDates(taskId) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  let workingDaysAdded = 0;
  let currentDate = new Date(today);
  let endDate = null;
  
  while (workingDaysAdded < 5) {
    currentDate.setDate(currentDate.getDate() + 1);
    const dayOfWeek = currentDate.getDay();
    
    if (dayOfWeek !== 0 && dayOfWeek !== 6) {
      workingDaysAdded++;
    }
    
    if (workingDaysAdded === 5) {
      endDate = new Date(currentDate);
    }
  }
  
  const startDateStr = formatDate(today);
  const endDateStr = formatDate(endDate);
  
  console.log(`📅 Assigning dates to task ${taskId}: ${startDateStr} - ${endDateStr}`);
  
  updateTaskDates(taskId, startDateStr, endDateStr);
}

// Gantt Bar Interactions
function setupGanttBarInteractions() {
  let draggedBar = null;
  let dragMode = null; // 'move', 'resize-left', 'resize-right'
  let startX = 0;
  let startLeft = 0;
  let startWidth = 0;
  let taskId = null;
  
  const edgeThreshold = 8; // pixels
  
  document.addEventListener('mousedown', (e) => {
    // Don't start bar drag if clicking on junction point
    if (e.target.closest('.junction-point')) return;
    
    const bar = e.target.closest('.gantt-bar');
    if (!bar) return;
    
    // Don't drag if junction dragging is active
    if (isDraggingJunction) return;
    
    const rect = bar.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    
    draggedBar = bar;
    taskId = bar.getAttribute('data-task-id');
    startX = e.clientX;
    startLeft = parseInt(bar.style.left);
    startWidth = parseInt(bar.style.width);
    
    if (mouseX < edgeThreshold) {
      dragMode = 'resize-left';
      bar.style.cursor = 'w-resize';
    } else if (mouseX > rect.width - edgeThreshold) {
      dragMode = 'resize-right';
      bar.style.cursor = 'e-resize';
    } else {
      dragMode = 'move';
      bar.style.cursor = 'grabbing';
    }
    
    bar.classList.add(dragMode === 'move' ? 'dragging' : 'resizing');
    e.preventDefault();
  });
  
  document.addEventListener('mousemove', (e) => {
    // Don't handle bar drag if junction dragging is active
    if (isDraggingJunction) return;
    
    if (!draggedBar) {
      // Update cursor on hover
      const bar = e.target.closest('.gantt-bar');
      if (bar) {
        const rect = bar.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        
        if (mouseX < edgeThreshold) {
          bar.style.cursor = 'w-resize';
        } else if (mouseX > rect.width - edgeThreshold) {
          bar.style.cursor = 'e-resize';
        } else {
          bar.style.cursor = 'move';
        }
      }
      return;
    }
    
    const deltaX = e.clientX - startX;
    const deltaInDays = Math.round(deltaX / dayWidth);
    
    if (dragMode === 'move') {
      const newLeft = startLeft + (deltaInDays * dayWidth);
      draggedBar.style.left = `${newLeft}px`;
    } else if (dragMode === 'resize-left') {
      const newLeft = startLeft + (deltaInDays * dayWidth);
      const newWidth = startWidth - (deltaInDays * dayWidth);
      
      if (newWidth >= dayWidth) {
        draggedBar.style.left = `${newLeft}px`;
        draggedBar.style.width = `${newWidth}px`;
      }
    } else if (dragMode === 'resize-right') {
      const newWidth = startWidth + (deltaInDays * dayWidth);
      
      if (newWidth >= dayWidth) {
        draggedBar.style.width = `${newWidth}px`;
      }
    }
  });
  
  document.addEventListener('mouseup', (e) => {
    // Don't handle bar drag if junction dragging is active
    if (isDraggingJunction) return;
    
    if (!draggedBar) return;
    
    const deltaX = e.clientX - startX;
    const deltaInDays = Math.round(deltaX / dayWidth);
    
    if (deltaInDays !== 0) {
      const task = ganttData.find(t => t.id == taskId);
      if (task && task.start && task.end) {
        const startDate = new Date(task.start);
        const endDate = new Date(task.end);
        
        if (dragMode === 'move') {
          startDate.setDate(startDate.getDate() + deltaInDays);
          endDate.setDate(endDate.getDate() + deltaInDays);
        } else if (dragMode === 'resize-left') {
          startDate.setDate(startDate.getDate() + deltaInDays);
        } else if (dragMode === 'resize-right') {
          endDate.setDate(endDate.getDate() + deltaInDays);
        }
        
        updateTaskDates(taskId, formatDate(startDate), formatDate(endDate));
      }
    }
    
    draggedBar.classList.remove('dragging', 'resizing');
    draggedBar.style.cursor = 'move';
    draggedBar = null;
    dragMode = null;
    taskId = null;
  });
}

function updateTaskDates(issueId, startDate, dueDate) {
  const url = `/projects/${projectId}/advanced_gantt/update_dates`;
  
  const csrfToken = getCSRFToken();
  
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': csrfToken
    },
    body: JSON.stringify({
      issue_id: issueId,
      start_date: startDate,
      due_date: dueDate
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log('✅ Task dates updated successfully');
      
      // Update local data
      const task = ganttData.find(t => t.id == issueId);
      if (task) {
        task.start = startDate;
        task.end = dueDate;
      }
      
      // Update task list
      updateTaskListDates(issueId, startDate, dueDate);
      
      // Redraw dependencies
      setTimeout(() => renderDependencies(), 50);
      
      showNotification('Task dates updated successfully', 'success');
    } else {
      console.error('❌ Error updating task dates:', data.error);
      showNotification('Error updating task dates', 'error');
      
      // Reload to revert changes
      setTimeout(() => location.reload(), 2000);
    }
  })
  .catch(error => {
    console.error('❌ Error updating task dates:', error);
    showNotification('Error updating task dates', 'error');
    
    // Reload to revert changes
    setTimeout(() => location.reload(), 2000);
  });
}

function updateTaskListDates(issueId, startDate, dueDate) {
  const taskRow = document.getElementById(`task-row-${issueId}`);
  if (!taskRow) return;
  
  const startCell = taskRow.querySelector('.task-start-cell');
  const dueCell = taskRow.querySelector('.task-due-cell');
  const durationCell = taskRow.querySelector('.task-duration-cell');
  
  if (startCell) startCell.textContent = formatDate(new Date(startDate));
  if (dueCell) dueCell.textContent = formatDate(new Date(dueDate));
  
  if (durationCell) {
    const start = new Date(startDate);
    const end = new Date(dueDate);
    const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
    durationCell.textContent = `${days}d`;
  }
}

function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute('content') : '';
}

function showNotification(message, type = 'success') {
  const notification = document.createElement('div');
  notification.className = `gantt-notification ${type}`;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

function showError(message) {
  console.error('❌', message);
  showNotification(message, 'error');
}

// Setup functions
function setupEventListeners() {
  // Today button
  const todayBtn = document.getElementById('today-btn');
  if (todayBtn) {
    todayBtn.addEventListener('click', () => {
      console.log('📅 Scrolling to today');
      const todayLine = document.querySelector('.gantt-grid-line.today');
      if (todayLine) {
        todayLine.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
      }
    });
  }
  
  // Create Dependency button
  setupDependencyCreation();
}

function setupResizer() {
  const resizer = document.getElementById('gantt-resizer');
  const leftPanel = document.getElementById('gantt-task-list-panel');
  const rightPanel = document.getElementById('gantt-chart-panel');
  
  if (!resizer || !leftPanel || !rightPanel) return;
  
  let isResizing = false;
  let startX = 0;
  let startWidth = 0;
  
  resizer.addEventListener('mousedown', (e) => {
    isResizing = true;
    startX = e.clientX;
    startWidth = leftPanel.offsetWidth;
    document.body.style.cursor = 'col-resize';
    e.preventDefault();
  });
  
  document.addEventListener('mousemove', (e) => {
    if (!isResizing) return;
    
    const delta = e.clientX - startX;
    const newWidth = startWidth + delta;
    
    if (newWidth >= 200 && newWidth <= 800) {
      leftPanel.style.flex = `0 0 ${newWidth}px`;
    }
  });
  
  document.addEventListener('mouseup', () => {
    if (isResizing) {
      isResizing = false;
      document.body.style.cursor = '';
      
      // Redraw dependencies after resize
      setTimeout(() => renderDependencies(), 50);
    }
  });
}

function setupColumnResizers() {
  const handles = document.querySelectorAll('.column-resizer-handle');
  
  handles.forEach(handle => {
    let isResizing = false;
    let startX = 0;
    let startWidth = 0;
    let column = null;
    
    handle.addEventListener('mousedown', (e) => {
      isResizing = true;
      startX = e.clientX;
      
      const columnName = handle.getAttribute('data-column');
      column = handle.closest('th');
      startWidth = column.offsetWidth;
      
      document.body.style.cursor = 'col-resize';
      e.preventDefault();
      e.stopPropagation();
    });
    
    document.addEventListener('mousemove', (e) => {
      if (!isResizing) return;
      
      const delta = e.clientX - startX;
      const newWidth = startWidth + delta;
      
      if (newWidth >= 50) {
        column.style.width = `${newWidth}px`;
        
        // Update corresponding body cells
        const columnName = handle.getAttribute('data-column');
        const cellClass = columnName.replace('task-', 'task-') + '-cell';
        const cells = document.querySelectorAll(`.${cellClass}`);
        
        cells.forEach(cell => {
          cell.style.width = `${newWidth}px`;
        });
      }
    });
    
    document.addEventListener('mouseup', () => {
      if (isResizing) {
        isResizing = false;
        document.body.style.cursor = '';
        column = null;
      }
    });
  });
}

function setupScrollSync() {
  const taskListBody = document.getElementById('task-list-body');
  const ganttChartPanel = document.getElementById('gantt-chart-panel');
  
  if (!taskListBody || !ganttChartPanel) return;
  
  let isSyncingLeft = false;
  let isSyncingRight = false;
  
  taskListBody.addEventListener('scroll', () => {
    if (!isSyncingLeft) {
      isSyncingRight = true;
      ganttChartPanel.scrollTop = taskListBody.scrollTop;
      setTimeout(() => { isSyncingRight = false; }, 10);
    }
  });
  
  ganttChartPanel.addEventListener('scroll', () => {
    if (!isSyncingRight) {
      isSyncingLeft = true;
      taskListBody.scrollTop = ganttChartPanel.scrollTop;
      setTimeout(() => { isSyncingLeft = false; }, 10);
    }
  });
}

function getMonthsInRange(startDate, endDate) {
  const months = [];
  let current = new Date(startDate);
  
  while (current <= endDate) {
    const year = current.getFullYear();
    const month = current.getMonth();
    const monthStart = new Date(year, month, 1);
    const monthEnd = new Date(year, month + 1, 0);
    
    const rangeStart = current < monthStart ? monthStart : current;
    const rangeEnd = monthEnd < endDate ? monthEnd : endDate;
    
    const days = Math.ceil((rangeEnd - rangeStart) / (1000 * 60 * 60 * 24)) + 1;
    
    months.push({
      label: `${monthStart.toLocaleDateString('en-US', { month: 'short' })} ${year}`,
      days: days
    });
    
    current = new Date(year, month + 1, 1);
  }
  
  return months;
}

// ============================================
// JUNCTION POINT DRAG & DROP DEPENDENCY CREATION
// ============================================

let isDraggingJunction = false;
let dragSourceJunction = null;
let dragSourceBar = null;
let dragSourceType = null; // 'start' or 'end'
let dragPreviewArrow = null;

function setupDependencyCreation() {
  // Setup junction point drag handlers
  setupJunctionPointDragDrop();
}

function setupJunctionPointDragDrop() {
  console.log('🔗 Setting up junction point drag & drop');
  
  // Use event delegation for junction points
  document.addEventListener('mousedown', handleJunctionMouseDown);
  document.addEventListener('mousemove', handleJunctionMouseMove);
  document.addEventListener('mouseup', handleJunctionMouseUp);
}

function handleJunctionMouseDown(e) {
  const junction = e.target.closest('.junction-point');
  if (!junction) return;
  
  e.preventDefault();
  e.stopPropagation();
  
  isDraggingJunction = true;
  dragSourceJunction = junction;
  dragSourceBar = junction.closest('.gantt-bar');
  dragSourceType = junction.getAttribute('data-junction-type');
  
  // Disable bar dragging/resizing while junction dragging
  dragSourceBar.style.pointerEvents = 'none';
  
  // Mark source bar
  dragSourceBar.classList.add('drag-source');
  junction.classList.add('active');
  
  console.log(`🎯 Started dragging from ${dragSourceType} junction of task ${dragSourceBar.getAttribute('data-task-id')}`);
}

function handleJunctionMouseMove(e) {
  if (!isDraggingJunction) return;
  
  e.preventDefault();
  
  // Update preview arrow
  updateJunctionPreviewArrow(e);
  
  // Detect hover over other bars
  const elementUnderMouse = document.elementFromPoint(e.clientX, e.clientY);
  const targetBar = elementUnderMouse?.closest('.gantt-bar');
  
  // Remove previous target highlighting
  document.querySelectorAll('.gantt-bar.drag-target').forEach(bar => {
    if (bar !== targetBar) {
      bar.classList.remove('drag-target');
      bar.querySelectorAll('.junction-point.drop-target').forEach(jp => {
        jp.classList.remove('drop-target');
      });
    }
  });
  
  if (targetBar && targetBar !== dragSourceBar) {
    targetBar.classList.add('drag-target');
    
    // Find closest junction point
    const junctions = targetBar.querySelectorAll('.junction-point');
    let closestJunction = null;
    let minDistance = Infinity;
    
    junctions.forEach(jp => {
      const rect = jp.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const distance = Math.sqrt(Math.pow(e.clientX - centerX, 2) + Math.pow(e.clientY - centerY, 2));
      
      if (distance < minDistance) {
        minDistance = distance;
        closestJunction = jp;
      }
    });
    
    // Highlight closest junction
    junctions.forEach(jp => jp.classList.remove('drop-target'));
    if (closestJunction && minDistance < 50) {
      closestJunction.classList.add('drop-target');
    }
  }
}

function handleJunctionMouseUp(e) {
  if (!isDraggingJunction) return;
  
  e.preventDefault();
  
  // Find target junction
  const elementUnderMouse = document.elementFromPoint(e.clientX, e.clientY);
  const targetJunction = elementUnderMouse?.closest('.junction-point.drop-target');
  
  if (targetJunction) {
    const targetBar = targetJunction.closest('.gantt-bar');
    const targetTaskId = targetBar.getAttribute('data-task-id');
    const sourceTaskId = dragSourceBar.getAttribute('data-task-id');
    const targetType = targetJunction.getAttribute('data-junction-type');
    
    if (targetTaskId !== sourceTaskId) {
      // Determine dependency type based on junction types
      const relationType = getDependencyType(dragSourceType, targetType);
      
      console.log(`✅ Creating dependency: ${sourceTaskId} (${dragSourceType}) -> ${targetTaskId} (${targetType}) = ${relationType}`);
      
      // Create dependency
      createDependencyFromJunctions(sourceTaskId, targetTaskId, relationType);
    }
  }
  
  // Clean up
  cleanupJunctionDrag();
}

function updateJunctionPreviewArrow(e) {
  const svg = document.getElementById('gantt-dependencies-svg');
  if (!svg) return;
  
  // Remove old preview
  const oldPreview = svg.querySelector('.dependency-preview-arrow');
  if (oldPreview) oldPreview.remove();
  
  const sourceRect = dragSourceJunction.getBoundingClientRect();
  const svgRect = svg.getBoundingClientRect();
  
  // Calculate source point from center of junction bubble
  let fromX, fromY;
  fromX = sourceRect.left + sourceRect.width / 2 - svgRect.left;
  fromY = sourceRect.top + sourceRect.height / 2 - svgRect.top;
  
  const toX = e.clientX - svgRect.left;
  const toY = e.clientY - svgRect.top;
  
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  const midX = (fromX + toX) / 2;
  const pathData = `M ${fromX} ${fromY} L ${midX} ${fromY} L ${midX} ${toY} L ${toX} ${toY}`;
  
  path.setAttribute('d', pathData);
  path.setAttribute('class', 'dependency-preview-arrow');
  path.setAttribute('marker-end', 'url(#arrowhead)');
  
  svg.appendChild(path);
}

function cleanupJunctionDrag() {
  isDraggingJunction = false;
  
  if (dragSourceBar) {
    dragSourceBar.classList.remove('drag-source');
    // Re-enable bar pointer events
    dragSourceBar.style.pointerEvents = '';
  }
  
  if (dragSourceJunction) {
    dragSourceJunction.classList.remove('active');
  }
  
  document.querySelectorAll('.gantt-bar.drag-target').forEach(bar => {
    bar.classList.remove('drag-target');
  });
  
  document.querySelectorAll('.junction-point.drop-target').forEach(jp => {
    jp.classList.remove('drop-target');
  });
  
  // Remove preview arrow
  const svg = document.getElementById('gantt-dependencies-svg');
  if (svg) {
    const preview = svg.querySelector('.dependency-preview-arrow');
    if (preview) preview.remove();
  }
  
  dragSourceJunction = null;
  dragSourceBar = null;
  dragSourceType = null;
}

function getDependencyType(sourceType, targetType) {
  // Determine Redmine relation type based on junction points
  if (sourceType === 'end' && targetType === 'start') {
    return 'precedes'; // Finish-to-Start (FS) - most common
  } else if (sourceType === 'end' && targetType === 'end') {
    return 'blocks'; // Finish-to-Finish (FF)
  } else if (sourceType === 'start' && targetType === 'start') {
    return 'relates'; // Start-to-Start (SS)
  } else if (sourceType === 'start' && targetType === 'end') {
    return 'duplicates'; // Start-to-Finish (SF)
  }
  return 'precedes'; // Default
}

function createDependencyFromJunctions(fromTaskId, toTaskId, relationType) {
  // Check if dependency already exists
  const existingDeps = dependenciesMap.get(fromTaskId) || [];
  if (existingDeps.includes(toTaskId)) {
    showNotification('Dependency already exists', 'error');
    return;
  }
  
  createDependency(fromTaskId, toTaskId, relationType, 0);
}

function createDependency(fromTaskId, toTaskId, relationType, delay) {
  console.log(`🔗 Creating dependency: ${fromTaskId} -> ${toTaskId} (${relationType}, delay: ${delay})`);
  console.log(`📍 Project ID: ${projectId}`);
  
  const url = `/projects/${projectId}/advanced_gantt/create_dependency`;
  const csrfToken = getCSRFToken();
  
  console.log(`📡 URL: ${url}`);
  console.log(`🔑 CSRF Token: ${csrfToken ? 'present' : 'missing'}`);
  
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': csrfToken
    },
    body: JSON.stringify({
      issue_from_id: fromTaskId,
      issue_to_id: toTaskId,
      relation_type: relationType,
      delay: delay
    })
  })
  .then(response => {
    console.log('📡 Response status:', response.status);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return response.json();
  })
  .then(data => {
    if (data.success) {
      console.log('✅ Dependency created successfully');
      
      // Update local map
      if (!dependenciesMap.has(fromTaskId)) {
        dependenciesMap.set(fromTaskId, []);
      }
      dependenciesMap.get(fromTaskId).push(toTaskId);
      
      // Redraw dependencies
      renderDependencies();
      
      showNotification('Dependency created successfully!', 'success');
    } else {
      console.error('❌ Error creating dependency:', data.error);
      showNotification('Error creating dependency: ' + data.error, 'error');
    }
  })
  .catch(error => {
    console.error('❌ Error creating dependency:', error);
    showNotification('Error creating dependency: ' + error.message, 'error');
  });
}

