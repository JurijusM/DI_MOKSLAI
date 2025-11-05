Redmine::Plugin.register :redmine_advanced_gantt do
  name 'Redmine Advanced Gantt Plugin'
  author 'Your Name'
  description 'Advanced Gantt chart with drag & drop, dependencies, and SVG rendering'
  version '1.0.0'
  url 'https://example.com'
  author_url 'https://example.com'

  project_module :advanced_gantt do
    permission :view_advanced_gantt, { gantt_advanced: [:show, :data] }
    permission :edit_advanced_gantt, { gantt_advanced: [:update_dates, :update_progress] }
  end

  menu :project_menu, :advanced_gantt, { controller: 'gantt_advanced', action: 'show' }, 
       caption: 'Advanced Gantt', after: :gantt, param: :project_id
end


