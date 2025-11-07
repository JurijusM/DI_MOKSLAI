RedmineApp::Application.routes.draw do
  get 'projects/:project_id/resource_planner', to: 'resource_planner#index', as: :project_resource_planner
end

