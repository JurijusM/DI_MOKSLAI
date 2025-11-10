RedmineApp::Application.routes.draw do
  get 'projects/:project_id/resource_planner', to: 'resource_planner#index', as: :project_resource_planner
  post 'projects/:project_id/resource_planner/assign', to: 'resource_planner#assign', as: :project_resource_planner_assign
  patch 'projects/:project_id/resource_planner/capacity', to: 'resource_planner#update_capacity', as: :project_resource_planner_capacity
end

