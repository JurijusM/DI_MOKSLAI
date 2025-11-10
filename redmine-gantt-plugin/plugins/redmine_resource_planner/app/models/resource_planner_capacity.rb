class ResourcePlannerCapacity < ActiveRecord::Base
  belongs_to :user

  validates :user_id, presence: true, uniqueness: true
  validates :hours_per_week, numericality: { greater_than_or_equal_to: 0, less_than: 10_000 }

  DEFAULT_CAPACITY = 40.0

  def self.for_users(user_ids)
    where(user_id: user_ids).index_by(&:user_id)
  end

  def self.default_hours
    DEFAULT_CAPACITY
  end

  def hours_per_week=(value)
    super(value.present? ? value : DEFAULT_CAPACITY)
  end
end

