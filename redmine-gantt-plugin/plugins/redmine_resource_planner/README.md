# Redmine Resource Planner (prototype)

## Vision

Resource Planner builds on top of Redmine to provide a cockpit for balancing workload across consultants, developers, and project managers. Key goals:

- **Unified capacity view** – see planned hours per person across all projects.
- **Unassigned pool** – drag upcoming tasks to a resource and week.
- **Cross-project load** – identify over/underutilised people immediately.
- **Configurable rules** – weekly capacity, vacations, billable vs. non-billable ratios.

## MVP scope

- **Project tab**: a new `Resources` entry beside Gantt within each project.
- **People registry**: list project members first, with link to open cross-project view.
- **Weekly grid**: initial focus on week-level timeline (later expand to day/month).
- **Data sources**:
  - `users.capacity_hours_per_week` (custom field to add in Phase 1).
  - `issues.estimated_hours`, `start_date`, `due_date`, `assigned_to`.
  - `time_entries.hours` for spent time overlay (Phase 2).
- **Unassigned tasks panel**: open issues without assignee, grouped by project hierarchy.
- **Status indicators**: highlight overload (>100%), underload (<50%), no data.
- **Drag plan (Phase 2)**: dropping task adjusts assignment/dates and re-renders load.

## Roadmap

1. **Phase 0** – Base plugin scaffold, menu entry, placeholder view *(this commit)*.
2. **Phase 1** – Read-only workload dashboard (weekly cells, aggregated hours).
3. **Phase 2** – Drag-and-drop task assignment with automatic issue updates.
4. **Phase 3** – Capacity rules, warnings, approvals, export.

## Development

The plugin lives inside `plugins/redmine_resource_planner`. Standard Redmine plugin conventions apply:

```bash
bundle exec rails server          # from container
rake redmine:plugins:migrate      # when migrations are added
```

*Status: experimental prototype.*

