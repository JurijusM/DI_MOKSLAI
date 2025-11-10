# Redmine Agile Board

Kanban-style board for Redmine projects. Provides configurable columns mapped to issue statuses, drag-and-drop issue movement, and a foundation for automatic time tracking when issues enter the In Progress column.

## Setup

1. Enable the module per project (Settings â†’ Modules â†’ Agile board).
2. Run undle exec rake redmine:plugins:assets (or restart Docker so assets are copied).
3. Visit the new "Agile board" tab in the project menu.
