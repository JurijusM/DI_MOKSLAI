"""
Recommendations Page - Product recommendations after discovery
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from streamlit_app.services.hierarchy_service import HierarchyService
from backend.app.database import SessionLocal
from backend.app.services.hierarchy_recommendation_service import HierarchyRecommendationService

st.set_page_config(
    page_title="ITER - Recommendations",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Product Recommendations")
st.markdown("Based on your work item selections")

# Initialize session state
if 'organization_id' not in st.session_state:
    st.session_state.organization_id = 1

try:
    db = SessionLocal()
    rec_service = HierarchyRecommendationService(db)
    
    # Get recommendation summary
    summary = rec_service.get_final_recommendation_summary(st.session_state.organization_id)
    
    if not summary.get('all_recommendations'):
        st.info("No requirements selected yet. Please complete the discovery process in Process Selection.")
    else:
        # Primary ERP Recommendation
        st.markdown("## Primary ERP Recommendation")
        st.markdown("---")
        
        primary = summary.get('primary_erp')
        
        if primary:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"### ✅ {primary['product_name']}")
                st.markdown(f"**Recommendation:** {primary['recommendation']}")
                st.markdown(f"**Must Coverage:** {primary['must_coverage']:.1f}%")
            
            with col2:
                st.metric("Score", f"{primary['score']:.1f}%", delta=None)
            
            # Comparison with other primary ERPs
            st.markdown("#### Comparison with Other ERP Systems")
            
            all_recs = summary['all_recommendations']
            primary_erps = {k: v for k, v in all_recs.items() if v['is_primary_erp']}
            
            # Sort by score
            sorted_erps = sorted(primary_erps.items(), key=lambda x: x[1]['total_score'], reverse=True)
            
            for erp_code, erp_data in sorted_erps:
                with st.expander(f"{erp_data['erp_system_name']} - Score: {erp_data['total_score']:.1f}%"):
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("Must Coverage", f"{erp_data['must_coverage']['percentage']:.1f}%")
                    with col_b:
                        st.metric("Should Coverage", f"{erp_data['should_coverage']['percentage']:.1f}%")
                    with col_c:
                        st.metric("Could Coverage", f"{erp_data['could_coverage']['percentage']:.1f}%")
                    
                    st.markdown(f"**Recommendation:** {erp_data['recommendation_level']}")
                    
                    if erp_data['gaps']:
                        st.warning(f"Gaps: {len(erp_data['gaps'])} critical scenarios not covered")
        
        # CRM Decision
        st.markdown("---")
        st.markdown("## CRM Analysis")
        
        crm = summary.get('crm', {})
        
        if crm.get('needed'):
            st.success(f"✅ **CRM Needed:** {crm['product_name']}")
            st.markdown(f"**Score:** {crm['score']:.1f}%")
            st.markdown("Customer relationship management capabilities are required based on your selections.")
        else:
            st.info("ℹ️ CRM may not be necessary based on current requirements.")
        
        # Additional Products
        additional = summary.get('additional_products', {})
        
        if additional:
            st.markdown("---")
            st.markdown("## Additional Products")
            
            for product_code, product_data in additional.items():
                st.markdown(f"**{product_data['erp_system_name']}** - Score: {product_data['total_score']:.1f}%")
                st.markdown(f"_{product_data['recommendation_level']}_")
                st.markdown("")
    
    db.close()
    
except Exception as e:
    st.error(f"Error generating recommendations: {e}")
    import traceback
    st.code(traceback.format_exc())
















