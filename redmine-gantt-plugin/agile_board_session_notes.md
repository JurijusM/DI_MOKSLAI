# Agile Board Session Notes (2025-11-10)

## Summary
- Created new plugin edmine_agile_board providing a basic Kanban board (controller, views, assets, locales).
- Added hook wiring (hooks.rb) to load CSS/JS and ran ake redmine:plugins:assets to publish assets.
- Restored plugin after accidental deletion and re-applied asset compilation.
- Added explicit project routes for the board and reloaded routes.
- Resolved No route matches error triggered from other menus.
- Reverted menu registration to hash-based URL to fix undefined method to_model.
- Added en and en-GB locales to remove translation warnings.

## Outstanding Ideas
- Enhance column configuration (per project/sprint) and automate time tracking when issues enter In Progress.
- Polish UI (drag-and-drop feedback, swimlanes, filters).
