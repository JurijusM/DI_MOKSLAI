module RedmineAgileBoard
  class Column
    attr_reader :id, :name, :status_ids

    def initialize(id:, name:, status_ids: [])
      @id = id
      @name = name
      @status_ids = status_ids
    end

    def self.all_for_project(project)
      statuses = IssueStatus.sorted
      [
        new(id: :backlog, name: I18n.t("label_agile_board_backlog"), status_ids: statuses.first(1).pluck(:id)),
        new(id: :in_progress, name: I18n.t("label_agile_board_in_progress"), status_ids: statuses.offset(1).limit(2).pluck(:id)),
        new(id: :done, name: I18n.t("label_agile_board_done"), status_ids: statuses.last(1).pluck(:id))
      ]
    end

    def self.find(column_id)
      all_for_project(nil).detect { |column| column.id.to_s == column_id.to_s }
    end

    def apply!(issue, user)
      return false unless status_ids.present?

      issue.init_journal(user)
      issue.status_id = status_ids.first
      issue.start_date ||= Date.today if id.to_s == "in_progress"
      issue.save
    end
  end
end
