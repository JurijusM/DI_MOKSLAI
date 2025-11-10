class ResourcePlannerController < ApplicationController
  before_action :find_project
  before_action :authorize
  before_action :require_login, only: [:assign, :update_capacity]
  helper :resource_planner

  DEFAULT_WEEK_COUNT = 8
  MAX_WEEK_COUNT = 12

  def index
    @users = @project.users.order(:firstname, :lastname)
    @unassigned_issues = @project.issues.open.where(assigned_to_id: nil)
                                .includes(:tracker, :project)
                                .order(:due_date, :start_date, :id)
    @unassigned_by_tracker = group_unassigned_by_tracker(@unassigned_issues)
    @assignable_users = @project.assignable_users.order(:firstname, :lastname)

    load_capacities

    build_schedule_data
    @issue = Issue.new(project: @project)
  end

  def assign
    unless User.current.allowed_to?(:edit_issues, @project) || User.current.allowed_to?(:add_issue_watchers, @project)
      render json: { error: l(:resource_planner_assign_forbidden) }, status: :forbidden
      return
    end

    issue = @project.issues.open.find(params[:issue_id])
    user = @project.users.find(params[:user_id])

    Issue.transaction do
      issue.assigned_to = user
      issue.save!
    end

    respond_to do |format|
      format.json do
        render json: {
          success: true,
          issue_id: issue.id,
          user_id: user.id
        }
      end
      format.html do
        flash[:notice] = l(:notice_successful_update)
        redirect_to project_resource_planner_path(@project)
      end
    end
  rescue ActiveRecord::RecordNotFound
    respond_to do |format|
      format.json { render json: { error: l(:resource_planner_assign_not_found) }, status: :not_found }
      format.html do
        flash[:error] = l(:resource_planner_assign_not_found)
        redirect_to project_resource_planner_path(@project)
      end
    end
  rescue StandardError => e
    Rails.logger.error("[ResourcePlanner] Failed to assign issue: #{e.class} - #{e.message}")
    Rails.logger.error(e.backtrace.first(5).join("\n"))
    respond_to do |format|
      format.json { render json: { error: l(:resource_planner_assign_error) }, status: :unprocessable_entity }
      format.html do
        flash[:error] = l(:resource_planner_assign_error)
        redirect_to project_resource_planner_path(@project)
      end
    end
  end

  def update_capacity
    unless User.current.allowed_to?(:manage_resource_planner_capacities, @project)
      render json: { error: l(:resource_planner_capacity_forbidden) }, status: :forbidden
      return
    end

    user = @project.users.find(params[:user_id])
    hours = params[:hours_per_week].presence

    capacity = ResourcePlannerCapacity.find_or_initialize_by(user_id: user.id)
    capacity.hours_per_week = hours || ResourcePlannerCapacity.default_hours
    capacity.save!

    respond_to do |format|
      format.json do
        render json: {
          success: true,
          user_id: user.id,
          hours_per_week: capacity.hours_per_week.to_f
        }
      end
      format.html do
        flash[:notice] = l(:resource_planner_capacity_updated)
        redirect_to project_resource_planner_path(@project)
      end
    end
  rescue ActiveRecord::RecordNotFound
    respond_to do |format|
      format.json { render json: { error: l(:resource_planner_capacity_not_found) }, status: :not_found }
      format.html do
        flash[:error] = l(:resource_planner_capacity_not_found)
        redirect_to project_resource_planner_path(@project)
      end
    end
  rescue ActiveRecord::RecordInvalid => e
    respond_to do |format|
      format.json { render json: { error: e.record.errors.full_messages.join(', ') }, status: :unprocessable_entity }
      format.html do
        flash[:error] = e.record.errors.full_messages.join(', ')
        redirect_to project_resource_planner_path(@project)
      end
    end
  rescue StandardError => e
    Rails.logger.error("[ResourcePlanner] Failed to update capacity: #{e.class} - #{e.message}")
    Rails.logger.error(e.backtrace.first(5).join("\n"))
    respond_to do |format|
      format.json { render json: { error: l(:resource_planner_capacity_error) }, status: :unprocessable_entity }
      format.html do
        flash[:error] = l(:resource_planner_capacity_error)
        redirect_to project_resource_planner_path(@project)
      end
    end
  end

  private

  def find_project
    project_identifier = params[:project_id] || params[:id]
    @project = Project.find(project_identifier)
  end

  def build_schedule_data
    user_ids = @users.map(&:id)

    assignments = Issue.open
                       .where(assigned_to_id: user_ids)
                       .where.not(start_date: nil, due_date: nil)
                       .includes(:assigned_to, :project)

    @weeks = build_weeks(assignments)
    @assignments_by_user = assignments.group_by(&:assigned_to_id)

    @resource_rows = @users.map do |user|
      capacity_hours = (@capacities[user.id]&.hours_per_week || ResourcePlannerCapacity.default_hours).to_f
      issues = Array(@assignments_by_user[user.id])
      task_entries = Hash.new { |hash, issue_id| hash[issue_id] = { issue: nil, weekly: Array.new(@weeks.size) { 0.0 } } }

      weeks_range_start = @weeks.first[:start]
      weeks_range_end = @weeks.last[:end]
      total_range_days = [(weeks_range_end - weeks_range_start).to_i + 1, 1].max

      cells = @weeks.each_with_index.map do |week, week_index|
        week_start = week[:start]
        week_end = week[:end]

        total_hours = 0.0
        entries = []

        issues.each do |issue|
          allocated = distribute_hours_for_week(issue, week_start, week_end)
          next if allocated.zero?

          total_hours += allocated
          task_entry = task_entries[issue.id]
          task_entry[:issue] ||= issue
          task_entry[:weekly][week_index] += allocated
          entries << {
            issue: issue,
            allocation_hours: allocated.round(1)
          }
        end

        utilisation = capacity_hours.positive? ? (total_hours / capacity_hours) : nil

        {
          hours: total_hours.round(1),
          issue_count: entries.size,
          utilisation: utilisation,
          capacity_hours: capacity_hours,
          entries: entries
        }
      end

      tasks = task_entries.values.map do |data|
        issue = data[:issue]
        next unless issue

        weekly_hours = data[:weekly].map { |hours| hours.round(1) }
        task_start = issue.start_date || weeks_range_start
        task_end = issue.due_date || weeks_range_end
        start_offset_days = [(task_start - weeks_range_start).to_i, 0].max
        end_offset_days = [(task_end - weeks_range_start).to_i, 0].max
        bar_start_percent = (start_offset_days.to_f / total_range_days) * 100
        bar_width_percent = ([(end_offset_days - start_offset_days + 1), 1].max.to_f / total_range_days) * 100

        {
          issue: issue,
          start_date: issue.start_date,
          due_date: issue.due_date,
          estimated_hours: issue.estimated_hours,
          weekly_hours: weekly_hours,
          total_hours: weekly_hours.sum.round(1),
          gantt_start_percent: bar_start_percent.round(2),
          gantt_width_percent: bar_width_percent.round(2)
        }
      end.compact.sort_by { |task| task[:start_date] || Date.new(1900, 1, 1) }

      {
        user: user,
        capacity_hours: capacity_hours.round(1),
        cells: cells,
        tasks: tasks
      }
    end
  end

  def build_weeks(assignments)
    base_start = Date.today.beginning_of_week(:monday)

    relevant_dates = assignments.flat_map { |issue| [issue.start_date, issue.due_date] }.compact
    relevant_dates += @unassigned_issues.flat_map { |issue| [issue.start_date, issue.due_date] }.compact

    start_week = relevant_dates.any? ? [relevant_dates.min.beginning_of_week(:monday), base_start].min : base_start

    minimum_last_week = start_week + (DEFAULT_WEEK_COUNT - 1).weeks
    latest_week_from_data = relevant_dates.any? ? relevant_dates.max.beginning_of_week(:monday) : start_week
    last_week_start = [minimum_last_week, latest_week_from_data].max

    max_last_week = start_week + (MAX_WEEK_COUNT - 1).weeks
    last_week_start = [last_week_start, max_last_week].min

    weeks = []
    current = start_week
    while current <= last_week_start
      week_end = current + 6
      weeks << {
        start: current,
        end: week_end,
        label: l(:label_week),
        number: current.cweek,
        current: (current..week_end).cover?(Date.today)
      }
      current += 7
    end

    weeks
  end

  def group_unassigned_by_tracker(issues)
    grouped = issues.group_by(&:tracker)
    grouped.sort_by do |tracker, _|
      [(tracker&.position || Float::INFINITY), tracker&.name.to_s]
    end.to_h
  end

  def load_capacities
    user_ids = @users.map(&:id)
    if defined?(ResourcePlannerCapacity) && ResourcePlannerCapacity.table_exists?
      @capacities = ResourcePlannerCapacity.for_users(user_ids)
      @capacity_default = ResourcePlannerCapacity.default_hours
    else
      @capacities = {}
      @capacity_default = 40.0
    end
  rescue ActiveRecord::StatementInvalid
    @capacities = {}
    @capacity_default = 40.0
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

end

