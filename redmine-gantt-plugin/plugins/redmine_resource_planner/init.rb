require_relative 'lib/redmine_resource_planner/hooks'

Redmine::Plugin.register :redmine_resource_planner do
  name 'Redmine Resource Planner'
  author 'DI_MOKSLAI Team'
  description 'Resource allocation and capacity planning views on top of Redmine issues'
  version '0.1.0'
  url 'https://github.com/JurijusM/DI_MOKSLAI'
  author_url 'https://github.com/JurijusM'

  project_module :resource_planner do
    permission :view_resource_planner, { resource_planner: [:index] }, require: :member
  end

  menu :project_menu,
       :resource_planner,
       { controller: 'resource_planner', action: 'index' },
       caption: :label_resource_planner,
       after: :gantt,
       param: :project_id,
       if: proc { |project| project.module_enabled?(:resource_planner) }
end

