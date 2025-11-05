"""
Home Page - Welcome and Overview
"""

import streamlit as st

st.set_page_config(
    page_title="ITER - Home",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Welcome to ITER")
st.markdown("### Intelligent Technology Evaluation & Requirements")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **What is ITER?**
    
    ITER helps you quickly gather ERP requirements and get automated 
    product recommendations for Microsoft ERP solutions.
    
    **Key Features:**
    - ✅ Self-service process evaluation
    - ✅ Automated product recommendations (BC vs D365F)
    - ✅ CRM decision support
    - ✅ Progress tracking
    - ✅ Fit/gap analysis
    """)

with col2:
    st.success("""
    **Getting Started:**
    
    1. Navigate to **Process Selection** page
    2. Select your end-to-end process (Order to Cash, etc.)
    3. Evaluate business processes:
       - 🔴 Must Have
       - 🟡 Should Have
       - 🟢 Optional
       - ⚪ Not Needed
    4. View recommendations on the Recommendations page
    """)

st.markdown("---")

st.markdown("### 🚀 Ready to start your discovery?")
if st.button("Go to Process Selection →", type="primary", use_container_width=True):
    st.switch_page("pages/2_📋_Process_Selection.py")



