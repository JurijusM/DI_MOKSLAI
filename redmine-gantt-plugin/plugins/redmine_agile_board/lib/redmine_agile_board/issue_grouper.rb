module RedmineAgileBoard
  class IssueGrouper
    def initialize(query, columns, user)
      @query = query
      @columns = columns
      @user = user
    end

    def grouped_issues
      issues = collection
      @columns.each_with_object({}) do |column, hash|
        hash[column.id] = issues.select { |issue| column.status_ids.include?(issue.status_id) }
      end
    end

    private

    def collection
      scope = Issue.visible(@user)
      scope = scope.where(project: @query.project) if @query.project
      scope.includes(:assigned_to, :tracker, :status).to_a
    end
  end
end
