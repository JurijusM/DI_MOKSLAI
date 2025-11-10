module ResourcePlannerHelper
  LIGHT_THRESHOLD = 0.7
  MEDIUM_THRESHOLD = 1.0

  def resource_load_class(hours, capacity)
    return 'resource-cell--empty' if hours.zero?
    return 'resource-cell--no-capacity' if capacity.nil? || capacity <= 0

    utilisation = hours.to_f / capacity.to_f

    if utilisation <= LIGHT_THRESHOLD
      'resource-cell--light'
    elsif utilisation <= MEDIUM_THRESHOLD
      'resource-cell--medium'
    else
      'resource-cell--heavy'
    end
  end

  def resource_capacity_hours(user, capacities)
    record = capacities[user.id]
    (record&.hours_per_week || ResourcePlannerCapacity.default_hours).to_f
  end

  def resource_utilisation_percent(utilisation)
    return nil if utilisation.nil?
    (utilisation * 100).round(1)
  end
end



