"""
ITER - Main Streamlit Application
Entry point for the ITER application.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="ITER - ERP Requirements Discovery",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point."""
    
    # Header
    st.markdown('<div class="main-header">🎯 ITER - Intelligent Technology Evaluation & Requirements</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'organization_id' not in st.session_state:
        st.session_state.organization_id = 1  # Default org for now
    if 'user_id' not in st.session_state:
        st.session_state.user_id = 1  # Default user for now
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = True  # For now, skip auth
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Select Page",
        ["Home", "Process Selection", "Dashboard", "Recommendations", "Reports"]
    )
    
    # Route to appropriate page
    if page == "Home":
        show_home()
    elif page == "Process Selection":
        show_process_selection()
    elif page == "Dashboard":
        show_dashboard()
    elif page == "Recommendations":
        show_recommendations()
    elif page == "Reports":
        show_reports()

def show_home():
    """Home page."""
    st.header("🏠 Welcome to ITER")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **What is ITER?**
        
        ITER helps you quickly gather ERP requirements and get automated 
        product recommendations for Microsoft ERP solutions.
        
        **Key Features:**
        - ✅ Self-service process evaluation
        - ✅ Automated product recommendations
        - ✅ Progress tracking
        - ✅ Fit/gap analysis
        """)
    
    with col2:
        st.success("""
        **Getting Started:**
        
        1. Go to **Process Selection** page
        2. Select your end-to-end process
        3. Evaluate business processes (Must/Should/Optional)
        4. View recommendations
        
        **Quick Stats:**
        - Processes available: (Loading...)
        - Your progress: (Loading...)
        """)
    
    st.markdown("---")
    st.markdown("### Ready to start?")
    if st.button("🚀 Start Discovery", type="primary", use_container_width=True):
        st.switch_page("pages/2_📋_Process_Selection.py")

def show_process_selection():
    """Process selection page - placeholder."""
    st.header("📋 Process Selection")
    st.info("This page will be built next. Check the pages directory for the full implementation.")

def show_dashboard():
    """Dashboard page - placeholder."""
    st.header("📊 Dashboard")
    st.info("This page will show your progress and statistics.")

def show_recommendations():
    """Recommendations page - placeholder."""
    st.header("🎯 Recommendations")
    st.info("This page will show product recommendations (BC vs D365F, CRM decision, etc.)")

def show_reports():
    """Reports page - placeholder."""
    st.header("📄 Reports")
    st.info("This page will provide fit/gap analysis and export functionality.")

if __name__ == "__main__":
    main()



