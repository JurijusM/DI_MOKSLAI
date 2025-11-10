class AgileBoardController < ApplicationController
  before_action :find_project, :authorize

  def index
    @query = IssueQuery.new(name: :label_agile_board)
    @query.project = @project
    @columns = RedmineAgileBoard::Column.all_for_project(@project)
    @issues_by_column = RedmineAgileBoard::IssueGrouper.new(@query, @columns, User.current).grouped_issues
  end

  def update_status
    issue = Issue.visible.find(params[:issue_id])
    column = RedmineAgileBoard::Column.find(params[:column_id])

    if column.apply!(issue, User.current)
      render json: { success: true }
    else
      render json: { success: false, errors: issue.errors.full_messages }, status: :unprocessable_entity
    end
  end

  private

  def find_project
    @project = Project.find(params[:project_id])
  end
end
