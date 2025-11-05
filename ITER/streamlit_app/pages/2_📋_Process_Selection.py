"""
Process Selection Page - Hierarchical tree view with MoSCoW prioritization
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from streamlit_app.services.hierarchy_service import HierarchyService

st.set_page_config(
    page_title="ITER - Process Selection",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Process Selection")
st.markdown("Navigate the process hierarchy and select priorities for work items (MoSCoW)")

# Initialize session state
if 'organization_id' not in st.session_state:
    st.session_state.organization_id = 1
if 'user_id' not in st.session_state:
    st.session_state.user_id = 1

# Instructions
with st.expander("ℹ️ How to use"):
    st.markdown("""
    **Hierarchical Navigation:**
    1. Click ▶ to expand processes
    2. Navigate through: E2E → Area → Process → Scenario → Work Items
    3. Select priorities (MoSCoW) at the **lowest level** (Tasks, Configuration deliverables, etc.)
    
    **MoSCoW Prioritization:**
    - 🔴 **Must** - Critical, cannot proceed without
    - 🟡 **Should** - Important but not critical
    - 🟢 **Could** - Nice to have
    - ⚪ **Won't** - Not needed
    """)

st.markdown("---")


def render_tree_recursive(item_or_list, hs, requirements, level=0):
    """Recursively render tree nodes."""
    items = [item_or_list] if isinstance(item_or_list, dict) else item_or_list
    
    for item in items:
        indent = "　" * level
        has_children = item.get('children') and len(item['children']) > 0
        
        # Expandable state
        expand_key = f"expand_{item['id']}"
        if expand_key not in st.session_state:
            st.session_state[expand_key] = False
        
        # Determine if this is selectable (work items that can have MoSCoW)
        # Selectable: Scenarios and all work item types
        is_selectable = item.get('work_item_type') in [
            'Scenario',
            'Task', 
            'Configuration deliverable', 
            'Workshop', 
            'Document deliverable'
        ]
        
        # Create row
        if is_selectable:
            col1, col2 = st.columns([2, 1])
        else:
            col1 = st.columns(1)[0]
        
        with col1:
            # Build display name with type
            type_badge = f"[{item['work_item_type']}] " if item.get('work_item_type') else ""
            display_name = f"{type_badge}{item['name']}"
            
            if has_children:
                icon = "▼" if st.session_state[expand_key] else "▶"
                label = f"{indent}{icon} **{display_name}**"
                if st.button(label, key=f"btn_{item['id']}", use_container_width=True):
                    st.session_state[expand_key] = not st.session_state[expand_key]
            else:
                icon = "•" if not is_selectable else "○"
                st.markdown(f"{indent}{icon} {display_name}")
        
        # Priority selection for work items (MoSCoW as radio buttons)
        if is_selectable:
            with col2:
                current_priority = requirements.get(item['id'], None)
                
                # Radio buttons for MoSCoW (horizontal)
                priority_options = ['🔴 Must', '🟡 Should', '🟢 Could', '⚪ Won\'t']
                priority_values = ['must', 'should', 'could', 'wont']
                
                # Get current index (default to 0 if not set)
                if current_priority in priority_values:
                    current_idx = priority_values.index(current_priority)
                else:
                    current_idx = 0  # Default to 'must'
                
                selected = st.radio(
                    "MoSCoW",
                    priority_options,
                    index=current_idx,
                    key=f"priority_{item['id']}",
                    horizontal=True,
                    label_visibility="collapsed"
                )
                
                # Convert back to value
                if selected in priority_options:
                    selected_idx = priority_options.index(selected)
                    priority = priority_values[selected_idx]
                    
                    # Auto-save when selection changes
                    if current_priority != priority:
                        hs.save_requirement(
                            st.session_state.organization_id,
                            item['id'],
                            priority,
                            st.session_state.user_id
                        )
                        st.toast(f"Saved: {priority.capitalize()}", icon="✅")
        
        # Render children if expanded
        if has_children and st.session_state[expand_key]:
            render_tree_recursive(item['children'], hs, requirements, level + 1)
        
        if level == 0:
            st.markdown("---")


try:
    with HierarchyService() as hs:
        # Get E2E processes for filter
        e2e_processes = hs.get_e2e_processes()
        
        if not e2e_processes:
            st.warning("No data found. Please import BPC data first.")
            st.code("python scripts/recreate_db_and_import.bat")
        else:
            # E2E Process filter
            e2e_options = ["All"] + [p.name for p in e2e_processes]
            selected_e2e = st.selectbox("Filter by End-to-End Process", e2e_options)
            
            st.markdown("---")
            
            # Get hierarchy tree
            if selected_e2e == "All":
                # Show all E2E processes
                tree_data = hs.get_hierarchy_tree()
            else:
                # Show selected E2E process
                selected_e2e_obj = next((p for p in e2e_processes if p.name == selected_e2e), None)
                if selected_e2e_obj:
                    tree_data = hs.get_hierarchy_tree(selected_e2e_obj.id)
                else:
                    tree_data = []
            
            # Get existing requirements
            requirements = {r.hierarchy_item_id: r.priority for r in hs.get_all_requirements(st.session_state.organization_id)}
            
            # Render tree
            if tree_data:
                render_tree_recursive(tree_data[0] if selected_e2e != "All" else tree_data, hs, requirements, level=0)
            else:
                st.info("No data found for selected filter.")
            
except Exception as e:
    st.error(f"Error loading data: {e}")
    import traceback
    st.code(traceback.format_exc())
