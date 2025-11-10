"""
Hierarchy Recommendation Service - Product recommendations based on hierarchical work item selections
"""

from typing import Dict, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.models import ProcessHierarchy, HierarchyRequirement, ERPSystem

class HierarchyRecommendationService:
    """Service for calculating product recommendations from hierarchical work items."""
    
    # Priority weights for scoring
    MUST_WEIGHT = 0.7      # 70% weight for 'must' requirements
    SHOULD_WEIGHT = 0.25   # 25% weight for 'should' requirements
    COULD_WEIGHT = 0.05    # 5% weight for 'could' requirements
    
    # Product categories
    PRIMARY_ERP_PRODUCTS = ['BC', 'D365F', 'D365SCM', 'D365COMM']
    CRM_PRODUCTS = ['CRM', 'D365CS', 'D365FS']
    SPECIALIZED_PRODUCTS = ['D365PO', 'D365HR']
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_recommendations(self, organization_id: int) -> Dict[str, Dict]:
        """
        Calculate recommendations based on work item selections.
        
        Flow:
        1. Get all work item requirements
        2. Roll up to scenarios (find parent scenarios)
        3. Group scenarios by priority (must/should/could)
        4. Map scenarios to ERP systems
        5. Calculate coverage for each ERP system
        """
        # Get all work item requirements for organization
        work_item_reqs = self.db.query(HierarchyRequirement).filter(
            HierarchyRequirement.organization_id == organization_id
        ).all()
        
        if not work_item_reqs:
            return {}
        
        # Roll up to scenarios
        scenario_priorities = self._rollup_to_scenarios(work_item_reqs)
        
        # Get all ERP systems
        erp_systems = self.db.query(ERPSystem).all()
        
        recommendations = {}
        
        for erp_system in erp_systems:
            rec_data = self._calculate_product_score(
                erp_system,
                scenario_priorities
            )
            recommendations[erp_system.code] = rec_data
        
        return recommendations
    
    def _rollup_to_scenarios(self, work_item_reqs: List[HierarchyRequirement]) -> Dict[str, List[int]]:
        """
        Roll up work item selections to scenarios.
        
        Returns:
            Dict mapping priority to list of scenario IDs
        """
        scenario_priorities = {'must': set(), 'should': set(), 'could': set()}
        
        for req in work_item_reqs:
            # Get the work item
            work_item = self.db.query(ProcessHierarchy).filter(
                ProcessHierarchy.id == req.hierarchy_item_id
            ).first()
            
            if not work_item:
                continue
            
            # Find parent scenario (level 4)
            scenario = self._find_scenario_parent(work_item)
            
            if scenario:
                priority = req.priority
                if priority in scenario_priorities:
                    scenario_priorities[priority].add(scenario.id)
        
        # Convert sets to lists
        return {k: list(v) for k, v in scenario_priorities.items()}
    
    def _find_scenario_parent(self, item: ProcessHierarchy) -> ProcessHierarchy:
        """Find the scenario (level 4) parent of a work item."""
        current = item
        
        # Traverse up until we find level 4 (scenario)
        while current:
            if current.level == 4:  # Scenario level
                return current
            
            # Go to parent
            if current.parent_id:
                current = self.db.query(ProcessHierarchy).filter(
                    ProcessHierarchy.id == current.parent_id
                ).first()
            else:
                break
        
        return None
    
    def _calculate_product_score(self, erp_system: ERPSystem, scenario_priorities: Dict) -> Dict:
        """Calculate score for a single product."""
        
        # Find scenarios that map to this ERP system
        must_coverage = self._calculate_coverage(scenario_priorities['must'], erp_system.id)
        should_coverage = self._calculate_coverage(scenario_priorities['should'], erp_system.id)
        could_coverage = self._calculate_coverage(scenario_priorities['could'], erp_system.id)
        
        # Calculate weighted score
        total_score = (
            (must_coverage['percentage'] * self.MUST_WEIGHT) +
            (should_coverage['percentage'] * self.SHOULD_WEIGHT) +
            (could_coverage['percentage'] * self.COULD_WEIGHT)
        )
        
        # Find gaps
        gaps = self._identify_gaps(scenario_priorities['must'], erp_system.id)
        
        # Determine recommendation level
        recommendation_level = self._get_recommendation_level(total_score)
        
        return {
            'erp_system_id': erp_system.id,
            'erp_system_code': erp_system.code,
            'erp_system_name': erp_system.name,
            'total_score': round(total_score, 2),
            'must_coverage': must_coverage,
            'should_coverage': should_coverage,
            'could_coverage': could_coverage,
            'gaps': gaps,
            'recommendation_level': recommendation_level,
            'is_primary_erp': erp_system.code in self.PRIMARY_ERP_PRODUCTS,
            'is_crm': erp_system.code in self.CRM_PRODUCTS,
            'is_specialized': erp_system.code in self.SPECIALIZED_PRODUCTS
        }
    
    def _calculate_coverage(self, scenario_ids: List[int], erp_system_id: int) -> Dict:
        """Calculate how many scenarios are covered by this ERP system."""
        if not scenario_ids:
            return {
                'covered': 0,
                'total': 0,
                'percentage': 0.0,
                'covered_scenarios': []
            }
        
        covered_count = 0
        covered_scenarios = []
        
        for scenario_id in scenario_ids:
            # Get the scenario
            scenario = self.db.query(ProcessHierarchy).filter(
                ProcessHierarchy.id == scenario_id
            ).first()
            
            if scenario and scenario.erp_system_id == erp_system_id:
                covered_count += 1
                covered_scenarios.append(scenario_id)
        
        percentage = (covered_count / len(scenario_ids)) * 100 if scenario_ids else 0
        
        return {
            'covered': covered_count,
            'total': len(scenario_ids),
            'percentage': round(percentage, 2),
            'covered_scenarios': covered_scenarios
        }
    
    def _identify_gaps(self, must_scenario_ids: List[int], erp_system_id: int) -> List[Dict]:
        """Identify scenarios that are NOT covered by this ERP system."""
        gaps = []
        
        for scenario_id in must_scenario_ids:
            scenario = self.db.query(ProcessHierarchy).filter(
                ProcessHierarchy.id == scenario_id
            ).first()
            
            if scenario and scenario.erp_system_id != erp_system_id:
                gaps.append({
                    'scenario_id': scenario.id,
                    'scenario_name': scenario.name,
                    'sequence_id': scenario.sequence_id
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
    
    def get_final_recommendation_summary(self, organization_id: int) -> Dict:
        """
        Get complete recommendation summary.
        Shows: BC vs D365F vs D365SCM comparison, CRM decision, additional products.
        """
        recommendations = self.calculate_recommendations(organization_id)
        
        if not recommendations:
            return {
                'primary_erp': None,
                'crm': {'needed': False},
                'all_recommendations': {},
                'summary': "No requirements selected yet. Please complete the discovery process."
            }
        
        # Get primary ERP recommendation
        primary_recs = {k: v for k, v in recommendations.items() if v['is_primary_erp']}
        if primary_recs:
            primary_code, primary_rec = max(primary_recs.items(), key=lambda x: x[1]['total_score'])
        else:
            primary_code, primary_rec = None, None
        
        # Check CRM need
        crm_recs = {k: v for k, v in recommendations.items() if v['is_crm']}
        if crm_recs:
            crm_code, crm_rec = max(crm_recs.items(), key=lambda x: x[1]['total_score'])
            crm_needed = crm_rec['total_score'] >= 50
        else:
            crm_needed, crm_rec = False, None
        
        # Specialized products
        specialized_recs = {
            k: v for k, v in recommendations.items()
            if v['is_specialized'] and v['total_score'] >= 50
        }
        
        return {
            'primary_erp': {
                'product_code': primary_code,
                'product_name': primary_rec['erp_system_name'] if primary_rec else None,
                'score': primary_rec['total_score'] if primary_rec else 0,
                'recommendation': primary_rec['recommendation_level'] if primary_rec else None,
                'must_coverage': primary_rec['must_coverage']['percentage'] if primary_rec else 0,
            } if primary_rec else None,
            'crm': {
                'needed': crm_needed,
                'product_code': crm_rec['erp_system_code'] if crm_rec else None,
                'product_name': crm_rec['erp_system_name'] if crm_rec else None,
                'score': crm_rec['total_score'] if crm_rec else 0,
            },
            'additional_products': specialized_recs,
            'all_recommendations': recommendations
        }
















