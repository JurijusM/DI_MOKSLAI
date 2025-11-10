require "redmine"

require_relative "lib/redmine_agile_board"
require_relative "lib/redmine_agile_board/hooks"

Redmine::Plugin.register :redmine_agile_board do
  name "Redmine Agile Board"
  author "DI_MOKSLAI Team"
  description "Kanban-style board for visualizing Redmine issues by workflow state"
  version "0.1.0"
  url "https://github.com/JurijusM/DI_MOKSLAI"
  author_url "https://github.com/JurijusM"

  project_module :agile_board do
    permission :view_agile_board, { agile_board: [:index] }, require: :member
    permission :manage_agile_board, { agile_board: [:update_status, :settings] }, require: :member
  end

  menu :project_menu,
       :agile_board,
       { controller: "agile_board", action: "index" },
       caption: :label_agile_board,
       after: :gantt,
       param: :project_id,
       if: proc { |project| project.module_enabled?(:agile_board) }
end
