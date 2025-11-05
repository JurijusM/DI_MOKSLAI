"""
Recommendation Service - Calculates product recommendations based on customer requirements.
This service maps requirements to Microsoft ERP products and generates scores.
"""

from typing import Dict, List, Tuple
from sqlalchemy.orm import Session
from app.models.requirement import CustomerRequirement
from app.models.process import BusinessProcess, Scenario
from app.models.product import ERPSystem

class RecommendationService:
    """Service for calculating product recommendations."""
    
    # Priority weights for scoring
    MUST_WEIGHT = 0.7      # 70% weight for 'must' requirements
    SHOULD_WEIGHT = 0.25    # 25% weight for 'should' requirements
    OPTIONAL_WEIGHT = 0.05  # 5% weight for 'optional' requirements
    
    # Product categories for recommendations
    PRIMARY_ERP_PRODUCTS = ['BC', 'D365F', 'D365SCM', 'D365COMM']
    CRM_PRODUCTS = ['CRM', 'D365CS', 'D365FS']
    SPECIALIZED_PRODUCTS = ['D365PO', 'D365HR']
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_recommendations(self, organization_id: int) -> Dict[str, Dict]:
        """
        Calculate recommendations for all Microsoft products.
        
        Returns:
            Dict mapping product codes to recommendation data
        """
        # Get all requirements for organization
        requirements = self.db.query(CustomerRequirement).filter(
            CustomerRequirement.organization_id == organization_id
        ).all()
        
        # Separate by priority
        must_reqs = [r for r in requirements if r.priority == 'must']
        should_reqs = [r for r in requirements if r.priority == 'should']
        optional_reqs = [r for r in requirements if r.priority == 'optional']
        
        # Get all ERP systems
        erp_systems = self.db.query(ERPSystem).all()
        
        recommendations = {}
        
        for erp_system in erp_systems:
            rec_data = self._calculate_product_score(
                erp_system,
                must_reqs,
                should_reqs,
                optional_reqs
            )
            recommendations[erp_system.code] = rec_data
        
        return recommendations
    
    def _calculate_product_score(
        self,
        erp_system: ERPSystem,
        must_reqs: List[CustomerRequirement],
        should_reqs: List[CustomerRequirement],
        optional_reqs: List[CustomerRequirement]
    ) -> Dict:
        """Calculate score for a single product."""
        
        # Find scenarios that cover each requirement
        must_coverage = self._calculate_coverage(must_reqs, erp_system.id)
        should_coverage = self._calculate_coverage(should_reqs, erp_system.id)
        optional_coverage = self._calculate_coverage(optional_reqs, erp_system.id)
        
        # Calculate weighted score
        total_score = (
            (must_coverage['percentage'] * self.MUST_WEIGHT) +
            (should_coverage['percentage'] * self.SHOULD_WEIGHT) +
            (optional_coverage['percentage'] * self.OPTIONAL_WEIGHT)
        )
        
        # Find gaps (missing requirements)
        gaps = self._identify_gaps(must_reqs, erp_system.id)
        
        # Determine recommendation level
        recommendation_level = self._get_recommendation_level(total_score)
        
        return {
            'erp_system_id': erp_system.id,
            'erp_system_code': erp_system.code,
            'erp_system_name': erp_system.name,
            'total_score': round(total_score, 2),
            'must_coverage': must_coverage,
            'should_coverage': should_coverage,
            'optional_coverage': optional_coverage,
            'gaps': gaps,
            'recommendation_level': recommendation_level,
            'is_primary_erp': erp_system.code in self.PRIMARY_ERP_PRODUCTS,
            'is_crm': erp_system.code in self.CRM_PRODUCTS,
            'is_specialized': erp_system.code in self.SPECIALIZED_PRODUCTS
        }
    
    def _calculate_coverage(
        self,
        requirements: List[CustomerRequirement],
        erp_system_id: int
    ) -> Dict:
        """Calculate how many requirements are covered by this ERP system."""
        if not requirements:
            return {
                'covered': 0,
                'total': 0,
                'percentage': 0.0,
                'covered_processes': []
            }
        
        covered_count = 0
        covered_processes = []
        
        for req in requirements:
            # Check if this ERP system has scenarios for this process
            scenarios = self.db.query(Scenario).filter(
                Scenario.business_process_id == req.business_process_id,
                Scenario.erp_system_id == erp_system_id
            ).count()
            
            if scenarios > 0:
                covered_count += 1
                covered_processes.append(req.business_process_id)
        
        percentage = (covered_count / len(requirements)) * 100 if requirements else 0
        
        return {
            'covered': covered_count,
            'total': len(requirements),
            'percentage': round(percentage, 2),
            'covered_processes': covered_processes
        }
    
    def _identify_gaps(
        self,
        must_requirements: List[CustomerRequirement],
        erp_system_id: int
    ) -> List[Dict]:
        """Identify requirements that are NOT covered by this ERP system."""
        gaps = []
        
        for req in must_requirements:
            scenarios = self.db.query(Scenario).filter(
                Scenario.business_process_id == req.business_process_id,
                Scenario.erp_system_id == erp_system_id
            ).count()
            
            if scenarios == 0:
                # This is a gap - get process details
                process = self.db.query(BusinessProcess).filter(
                    BusinessProcess.id == req.business_process_id
                ).first()
                
                if process:
                    gaps.append({
                        'process_id': process.id,
                        'process_code': process.process_code,
                        'process_name': process.name,
                        'priority': req.priority
                    })
        
        return gaps
    
    def _get_recommendation_level(self, score: float) -> str:
        """Get recommendation level based on score."""
        if score >= 85:
            return "Highly Recommended"
        elif score >= 70:
            return "Recommended"
        elif score >= 50:
            return "Consider"
        elif score >= 30:
            return "May Not Be Suitable"
        else:
            return "Not Recommended"
    
    def get_primary_recommendation(self, recommendations: Dict[str, Dict]) -> Tuple[str, Dict]:
        """
        Get the primary ERP recommendation (BC, D365F, D365SCM, or D365COMM).
        
        Returns:
            Tuple of (product_code, recommendation_data)
        """
        primary_recs = {
            code: data for code, data in recommendations.items()
            if data.get('is_primary_erp', False)
        }
        
        if not primary_recs:
            return None, None
        
        # Sort by score and return best
        best = max(primary_recs.items(), key=lambda x: x[1]['total_score'])
        return best
    
    def is_crm_needed(self, recommendations: Dict[str, Dict], threshold: float = 50.0) -> Tuple[bool, Dict]:
        """
        Determine if CRM is needed based on requirements.
        
        Args:
            recommendations: Full recommendations dict
            threshold: Minimum score to consider CRM needed
        
        Returns:
            Tuple of (is_needed: bool, best_crm_recommendation: Dict)
        """
        crm_recs = {
            code: data for code, data in recommendations.items()
            if data.get('is_crm', False)
        }
        
        if not crm_recs:
            return False, None
        
        # Get best CRM product
        best_crm = max(crm_recs.items(), key=lambda x: x[1]['total_score'])
        crm_code, crm_data = best_crm
        
        is_needed = crm_data['total_score'] >= threshold
        
        return is_needed, crm_data
    
    def get_final_recommendation_summary(self, organization_id: int) -> Dict:
        """
        Get complete recommendation summary for an organization.
        This is the main function to call after discovery completion.
        
        Returns:
            Complete recommendation summary with:
            - Primary ERP recommendation
            - CRM decision
            - Additional products
            - Overall fit analysis
        """
        recommendations = self.calculate_recommendations(organization_id)
        
        # Get primary ERP
        primary_code, primary_rec = self.get_primary_recommendation(recommendations)
        
        # Check CRM need
        crm_needed, crm_rec = self.is_crm_needed(recommendations)
        
        # Get specialized products
        specialized_recs = {
            code: data for code, data in recommendations.items()
            if data.get('is_specialized', False) and data['total_score'] >= 50
        }
        
        return {
            'primary_erp': {
                'product_code': primary_code,
                'product_name': primary_rec['erp_system_name'] if primary_rec else None,
                'score': primary_rec['total_score'] if primary_rec else 0,
                'recommendation': primary_rec['recommendation_level'] if primary_rec else None,
                'must_coverage': primary_rec['must_coverage']['percentage'] if primary_rec else 0,
                'gaps_count': len(primary_rec['gaps']) if primary_rec else 0
            },
            'crm': {
                'needed': crm_needed,
                'product_code': crm_rec['erp_system_code'] if crm_rec else None,
                'product_name': crm_rec['erp_system_name'] if crm_rec else None,
                'score': crm_rec['total_score'] if crm_rec else 0,
                'recommendation': crm_rec['recommendation_level'] if crm_rec else None
            },
            'additional_products': specialized_recs,
            'all_recommendations': recommendations,
            'summary': self._generate_summary_text(primary_rec, crm_needed, crm_rec)
        }
    
    def _generate_summary_text(self, primary_rec: Dict, crm_needed: bool, crm_rec: Dict) -> str:
        """Generate human-readable summary text."""
        if not primary_rec:
            return "Unable to generate recommendation. Please complete more requirements."
        
        summary_parts = []
        
        # Primary ERP
        summary_parts.append(
            f"**Primary Recommendation: {primary_rec['erp_system_name']}** "
            f"(Score: {primary_rec['total_score']:.1f}%)"
        )
        summary_parts.append(
            f"This product covers {primary_rec['must_coverage']['percentage']:.1f}% "
            f"of your 'Must Have' requirements."
        )
        
        # Gaps
        if primary_rec['gaps']:
            summary_parts.append(
                f"Note: {len(primary_rec['gaps'])} critical requirements may require "
                f"additional solutions or customization."
            )
        
        # CRM
        if crm_needed:
            summary_parts.append(
                f"\n**CRM Recommended: {crm_rec['erp_system_name']}** "
                f"(Score: {crm_rec['total_score']:.1f}%)"
            )
            summary_parts.append(
                "Customer relationship management capabilities are required based on your selections."
            )
        else:
            summary_parts.append(
                "\nCRM may not be necessary based on current requirements."
            )
        
        return "\n".join(summary_parts)

