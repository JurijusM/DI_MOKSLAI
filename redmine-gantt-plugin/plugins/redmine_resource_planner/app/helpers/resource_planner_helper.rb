module ResourcePlannerHelper
  def resource_load_class(hours)
    return 'resource-cell--empty' if hours.zero?

    case hours
    when 0...10
      'resource-cell--light'
    when 10...20
      'resource-cell--medium'
    else
      'resource-cell--heavy'
    end
  end
end

