class GanttAdvancedController < ApplicationController
  before_action :find_project
  before_action :authorize, except: [:update_dates, :update_progress, :create_dependency]
  before_action :require_login, only: [:update_dates, :update_progress, :create_dependency]
  skip_before_action :verify_authenticity_token, only: [:update_dates, :update_progress, :create_dependency]

  def show
    @issues = @project.issues.includes(:assigned_to, :priority, :tracker, :status)
    @gantt_data = prepare_gantt_data(@issues)
  end

  def data
    issues = @project.issues.includes(:assigned_to, :priority, :tracker, :status, :relations)
    gantt_data = prepare_gantt_data(issues)
    render json: gantt_data
  end

  def update_dates
    issue = Issue.find(params[:issue_id])
    
    if issue.project_id != @project.id
      render json: { error: 'Unauthorized' }, status: :forbidden
      return
    end

    issue.start_date = Date.parse(params[:start_date]) if params[:start_date]
    issue.due_date = Date.parse(params[:due_date]) if params[:due_date]
    
    if issue.save
      render json: { success: true, issue: format_issue(issue) }
    else
      render json: { error: issue.errors.full_messages }, status: :unprocessable_entity
    end
  rescue => e
    render json: { error: e.message }, status: :internal_server_error
  end

  def update_progress
    issue = Issue.find(params[:issue_id])
    
    if issue.project_id != @project.id
      render json: { error: 'Unauthorized' }, status: :forbidden
      return
    end

    issue.done_ratio = params[:progress].to_i
    
    if issue.save
      render json: { success: true }
    else
      render json: { error: issue.errors.full_messages }, status: :unprocessable_entity
    end
  rescue => e
    render json: { error: e.message }, status: :internal_server_error
  end

  def create_dependency
    Rails.logger.info "🔗 Creating dependency: #{params[:issue_from_id]} -> #{params[:issue_to_id]}"
    Rails.logger.info "📍 Project: #{@project.inspect}"
    Rails.logger.info "📦 Params: #{params.inspect}"
    
    issue_from = Issue.find(params[:issue_from_id])
    issue_to = Issue.find(params[:issue_to_id])
    
    Rails.logger.info "✅ Found issues: #{issue_from.id} (project #{issue_from.project_id}) -> #{issue_to.id} (project #{issue_to.project_id})"
    
    # Validate both issues belong to the project
    if issue_from.project_id != @project.id || issue_to.project_id != @project.id
      Rails.logger.error "❌ Project mismatch: issue projects (#{issue_from.project_id}, #{issue_to.project_id}) vs @project (#{@project.id})"
      render json: { error: 'Unauthorized' }, status: :forbidden
      return
    end
    
    # Check for circular dependency
    if would_create_circular_dependency?(issue_from.id, issue_to.id)
      render json: { error: 'Cannot create circular dependency' }, status: :unprocessable_entity
      return
    end
    
    relation = IssueRelation.new(
      issue_from_id: params[:issue_from_id],
      issue_to_id: params[:issue_to_id],
      relation_type: params[:relation_type] || 'precedes',
      delay: params[:delay] || 0
    )
    
    Rails.logger.info "📝 Attempting to save relation: #{relation.inspect}"
    
    if relation.save
      Rails.logger.info "✅ Relation saved successfully! ID: #{relation.id}"
      
      render json: { 
        success: true, 
        relation_id: relation.id,
        from_id: relation.issue_from_id,
        to_id: relation.issue_to_id,
        relation_type: relation.relation_type
      }
    else
      Rails.logger.error "❌ Failed to save relation: #{relation.errors.full_messages.join(', ')}"
      render json: { error: relation.errors.full_messages }, status: :unprocessable_entity
    end
  rescue => e
    Rails.logger.error "💥 Exception in create_dependency: #{e.class}: #{e.message}"
    Rails.logger.error e.backtrace.join("\n")
    render json: { error: e.message }, status: :internal_server_error
  end

  private

  def find_project
    @project = Project.find(params[:project_id])
  rescue ActiveRecord::RecordNotFound
    render_404
  end

  def prepare_gantt_data(issues)
    issues.map do |issue|
      format_issue(issue)
    end
  end

  def format_issue(issue)
    {
      id: issue.id.to_s,
      name: issue.subject,
      start: issue.start_date&.strftime('%Y-%m-%d') || '',
      end: issue.due_date&.strftime('%Y-%m-%d') || '',
      progress: issue.done_ratio || 0,
      status: issue.status.name,
      status_class: status_class(issue.status.id),
      assigned_to: issue.assigned_to&.name || 'Unassigned',
      priority: issue.priority.name,
      dependencies: get_dependencies(issue)
    }
  end

  def get_dependencies(issue)
    issue.relations.select { |r| r.relation_type == 'precedes' }.map do |relation|
      relation.issue_to_id.to_s
    end
  end

  def status_class(status_id)
    case status_id
    when 1 then 'gantt-new'
    when 2 then 'gantt-progress'
    when 3 then 'gantt-resolved'
    when 5 then 'gantt-closed'
    else 'gantt-new'
    end
  end

  def would_create_circular_dependency?(from_id, to_id)
    # Check if to_id already leads to from_id
    visited = Set.new
    queue = [to_id]
    
    while !queue.empty?
      current_id = queue.shift
      return true if current_id == from_id
      
      next if visited.include?(current_id)
      visited.add(current_id)
      
      # Get all issues that current_id depends on
      IssueRelation.where(issue_from_id: current_id, relation_type: 'precedes').each do |rel|
        queue << rel.issue_to_id
      end
    end
    
    false
  end
end

