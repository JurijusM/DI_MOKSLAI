document.addEventListener('DOMContentLoaded', function () {
  const container = document.querySelector('.resource-planner');
  if (!container) {
    return;
  }

  console.debug('[ResourcePlanner] script initialised');

  const summaryHeader = container.querySelector('.resource-grid__summary-header');
  if (summaryHeader) {
    const width = summaryHeader.getBoundingClientRect().width;
    container.style.setProperty('--summary-width', `${Math.round(width)}px`);
  }

  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content || container.dataset.csrfToken || '';

  const showStatus = (statusEl, message, type) => {
    if (!statusEl) {
      return;
    }
    statusEl.textContent = message || '';
    statusEl.classList.toggle('is-success', type === 'success');
    statusEl.classList.toggle('is-error', type === 'error');
    if (message) {
      setTimeout(() => {
        statusEl.textContent = '';
        statusEl.classList.remove('is-success', 'is-error');
      }, 2500);
    }
  };

  const capacityForms = container.querySelectorAll('.resource-planner__capacity-form');
  capacityForms.forEach((form) => {
    const input = form.querySelector('.resource-planner__capacity-input');
    const statusEl = form.querySelector('.resource-planner__capacity-status');
    const resetButton = form.querySelector('.resource-planner__capacity-reset');
    const defaultHours = resetButton ? parseFloat(resetButton.dataset.defaultHours) : null;

    resetButton?.addEventListener('click', (event) => {
      event.preventDefault();
      if (defaultHours !== null) {
        input.value = defaultHours;
        input.focus();
      }
    });

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const userId = form.dataset.userId;
      const hoursValue = input.value;
      const savingText = form.dataset.savingText || 'Saving…';
      const savedText = form.dataset.savedText || 'Saved';
      const errorText = form.dataset.errorText || 'Failed';

      showStatus(statusEl, savingText);

      try {
        const response = await fetch(form.action, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
            'X-CSRF-Token': csrfToken
          },
          body: JSON.stringify({
            user_id: userId,
            hours_per_week: hoursValue
          })
        });

        const payload = await response.json();

        if (!response.ok || !payload.success) {
          throw new Error(payload && payload.error ? payload.error : errorText);
        }

        input.value = parseFloat(payload.hours_per_week).toFixed(1);
        showStatus(statusEl, savedText, 'success');

        // Update row header label as well
        const rowHeader = container.querySelector(`.resource-planner__row[data-user-id="${userId}"] .resource-planner__capacity-label`);
        if (rowHeader) {
          rowHeader.textContent = `${parseFloat(payload.hours_per_week).toFixed(1)}h/week`;
        }
      } catch (error) {
        console.error('[ResourcePlanner] Capacity update failed', error);
        showStatus(statusEl, error.message || errorText, 'error');
      }
    });
  });

  const toggleButtons = container.querySelectorAll('.resource-planner__toggle-tasks');
  toggleButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const userId = button.dataset.userId;
      const panel = container.querySelector(`#resource-tasks-${userId}`);
      if (!panel) {
        console.warn('[ResourcePlanner] tasks panel not found for user', userId);
        return;
      }

      const row = button.closest('.resource-grid__resource');
      const bars = row ? row.querySelector('.resource-grid__task-bars') : null;

      const isVisible = panel.classList.toggle('is-visible');
      if (bars) {
        bars.classList.toggle('is-visible', isVisible);
      }
      button.classList.toggle('is-expanded', isVisible);
      button.setAttribute('aria-expanded', isVisible ? 'true' : 'false');
      const icon = button.querySelector('.toggle-icon');
      if (icon) {
        icon.textContent = isVisible ? '-' : '+';
      }
      console.debug('[ResourcePlanner] toggle tasks panel', { userId, isVisible });
    });
  });
});



