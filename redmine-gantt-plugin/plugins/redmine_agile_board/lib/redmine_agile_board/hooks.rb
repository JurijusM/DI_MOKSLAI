module RedmineAgileBoard
  class Hooks < Redmine::Hook::ViewListener
    def view_layouts_base_html_head(_context)
      tags = []
      tags << stylesheet_link_tag("agile_board", plugin: "redmine_agile_board")
      tags << javascript_include_tag("agile_board", plugin: "redmine_agile_board")
      tags.join("\n").html_safe
    end
  end
end
