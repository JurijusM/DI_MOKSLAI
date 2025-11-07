class ResourcePlannerController < ApplicationController
  before_action :find_project
  before_action :authorize
  helper :resource_planner

  def index
    @users = @project.users.order(:firstname, :lastname)
    @unassigned_issues = @project.issues.open.where(assigned_to_id: nil).includes(:tracker)

    build_schedule_data
  end

  private

  def find_project
    project_identifier = params[:project_id] || params[:id]
    @project = Project.find(project_identifier)
  end

  def build_schedule_data
    start_week = Date.today.beginning_of_week(:monday)
    week_count = 8
    @weeks = (0...week_count).map { |offset| start_week + offset.weeks }

    user_ids = @users.map(&:id)
    assignments_scope = Issue.open.where(assigned_to_id: user_ids)
                                 .where('start_date IS NOT NULL AND due_date IS NOT NULL')
                                 .includes(:assigned_to, :project)

    @assignments_by_user = assignments_scope.group_by(&:assigned_to_id)

    @resource_rows = @users.map do |user|
      issues = @assignments_by_user[user.id] || []
      cells = @weeks.map do |week_start|
        week_end = week_start + 6
        hours = issues.sum do |issue|
          distribute_hours_for_week(issue, week_start, week_end)
        end
        { hours: hours.round(1), issue_count: issues_in_week(issues, week_start, week_end).count }
      end

      { user: user, cells: cells }
    end
  end

  def distribute_hours_for_week(issue, week_start, week_end)
    return 0.0 unless issue.start_date && issue.due_date && issue.estimated_hours

    issue_start = issue.start_date
    issue_end = issue.due_date
    overlap_start = [issue_start, week_start].max
    overlap_end = [issue_end, week_end].min

    return 0.0 if overlap_start > overlap_end

    total_days = (issue_end - issue_start + 1).to_i
    overlap_days = (overlap_end - overlap_start + 1).to_i
    return 0.0 if total_days <= 0

    (issue.estimated_hours.to_f * overlap_days) / total_days
  end

  def issues_in_week(issues, week_start, week_end)
    issues.select do |issue|
      issue.start_date && issue.due_date &&
        issue.start_date <= week_end && issue.due_date >= week_start
    end
  end
end

