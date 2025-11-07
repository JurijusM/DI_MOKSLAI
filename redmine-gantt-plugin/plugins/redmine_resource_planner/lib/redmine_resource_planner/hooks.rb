module RedmineResourcePlanner
  class Hooks < Redmine::Hook::ViewListener
    def view_layouts_base_html_head(_context)
      tags = []
      tags << stylesheet_link_tag('resource_planner', plugin: 'redmine_resource_planner')
      tags << javascript_include_tag('resource_planner', plugin: 'redmine_resource_planner')
      tags.join('\n').html_safe
    end
  end
end

