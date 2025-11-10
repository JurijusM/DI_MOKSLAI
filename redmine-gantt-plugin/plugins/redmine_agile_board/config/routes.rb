RedmineApp::Application.routes.draw do
  get 'projects/:project_id/agile_board', to: 'agile_board#index', as: :project_agile_board
  patch 'projects/:project_id/agile_board/update_status', to: 'agile_board#update_status', as: :project_agile_board_update_status

  get 'projects/:id/agile_board', to: 'agile_board#index'
  patch 'projects/:id/agile_board/update_status', to: 'agile_board#update_status'
end
