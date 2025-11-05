get 'projects/:project_id/advanced_gantt', to: 'gantt_advanced#show', as: 'project_advanced_gantt'
get 'projects/:project_id/advanced_gantt/data', to: 'gantt_advanced#data'
post 'projects/:project_id/advanced_gantt/update_dates', to: 'gantt_advanced#update_dates'
post 'projects/:project_id/advanced_gantt/update_progress', to: 'gantt_advanced#update_progress'
post 'projects/:project_id/advanced_gantt/create_dependency', to: 'gantt_advanced#create_dependency'

