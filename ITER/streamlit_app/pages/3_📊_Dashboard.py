"""
Dashboard Page - Progress tracking and statistics
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from streamlit_app.services.hierarchy_service import HierarchyService

st.set_page_config(
    page_title="ITER - Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Discovery Dashboard")

# Initialize session state
if 'organization_id' not in st.session_state:
    st.session_state.organization_id = 1

try:
    with HierarchyService() as hs:
        # Get statistics
        requirements = hs.get_all_requirements(st.session_state.organization_id)
        
        # Count by priority
        must_count = len([r for r in requirements if r.priority == 'must'])
        should_count = len([r for r in requirements if r.priority == 'should'])
        could_count = len([r for r in requirements if r.priority == 'could'])
        wont_count = len([r for r in requirements if r.priority == 'wont'])
        
        total = len(requirements)
        
        # Display statistics
        st.markdown("### 📈 Your Progress")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🔴 Must Have", must_count)
        with col2:
            st.metric("🟡 Should Have", should_count)
        with col3:
            st.metric("🟢 Could Have", could_count)
        with col4:
            st.metric("⚪ Won't Have", wont_count)
        
        st.markdown("---")
        
        # Total evaluated
        st.markdown("### 📋 Total Work Items Evaluated")
        st.metric("Total", total)
        
        if total == 0:
            st.info("No work items evaluated yet. Go to Process Selection to start!")
        else:
            # Show breakdown
            st.markdown("### Priority Breakdown")
            
            if total > 0:
                st.progress(must_count / total if total > 0 else 0, text=f"Must: {must_count} ({must_count/total*100:.1f}%)")
                st.progress(should_count / total if total > 0 else 0, text=f"Should: {should_count} ({should_count/total*100:.1f}%)")
                st.progress(could_count / total if total > 0 else 0, text=f"Could: {could_count} ({could_count/total*100:.1f}%)")
        
except Exception as e:
    st.error(f"Error loading dashboard: {e}")
    import traceback
    st.code(traceback.format_exc())
















