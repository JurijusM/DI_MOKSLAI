"""
Tree View Component - Hierarchical display with expand/collapse
"""

import streamlit as st
from typing import List, Dict, Any

def render_tree_node(item: Dict[str, Any], level_indent: int = 0, can_select: bool = False):
    """
    Render a single tree node with expand/collapse functionality.
    
    Args:
        item: Dictionary containing node data (id, name, level, children, etc.)
        level_indent: Indentation level for visual hierarchy
        can_select: Whether this node can have MoSCoW selection
    
    Returns:
        Selected priority if can_select, else None
    """
    indent = "　" * level_indent  # Full-width space for indentation
    has_children = item.get('children') and len(item.get('children', [])) > 0
    
    # Expand/collapse state
    expand_key = f"expand_{item['id']}"
    if expand_key not in st.session_state:
        st.session_state[expand_key] = False
    
    # Create container for this node
    with st.container():
        col1, col2 = st.columns([4, 1] if can_select else [1])
        
        with col1:
            # Expand/collapse button
            if has_children:
                icon = "▼" if st.session_state[expand_key] else "▶"
                if st.button(f"{indent}{icon} {item['name']}", key=f"btn_{item['id']}", use_container_width=True):
                    st.session_state[expand_key] = not st.session_state[expand_key]
            else:
                # Leaf node (no children)
                icon = "•" if not can_select else "○"
                st.markdown(f"{indent}{icon} **{item['name']}**")
            
            # Show metadata
            if item.get('work_item_type'):
                st.caption(f"{indent}　Type: {item['work_item_type']}")
            if item.get('sequence_id'):
                st.caption(f"{indent}　ID: {item['sequence_id']}")
        
        # MoSCoW selection for lowest level
        if can_select and col2:
            with col2:
                current_priority = item.get('current_priority', 'not_selected')
                priorities = ['must', 'should', 'could', 'wont']
                
                priority = st.selectbox(
                    "Priority",
                    priorities,
                    index=priorities.index(current_priority) if current_priority in priorities else 0,
                    key=f"priority_{item['id']}",
                    label_visibility="collapsed"
                )
                
                return priority
        
        # Render children if expanded
        if has_children and st.session_state[expand_key]:
            for child in item.get('children', []):
                # Determine if child can be selected (lowest level work items)
                child_can_select = child.get('level') >= 4 and child.get('work_item_type') in [
                    'Task', 'Configuration deliverable', 'Workshop', 'Document deliverable'
                ]
                render_tree_node(child, level_indent + 1, child_can_select)
    
    return None


def render_hierarchy_tree(root_items: List[Dict[str, Any]]):
    """
    Render full hierarchy tree.
    
    Args:
        root_items: List of root level items (E2E processes)
    """
    for root in root_items:
        render_tree_node(root, level_indent=0, can_select=False)











