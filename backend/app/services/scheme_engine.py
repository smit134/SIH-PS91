import json
import os
from typing import List
from app.models.financials import UserProfile, SchemeMatchItem

def load_schemes() -> List[dict]:
    # Adjust path relative to the script location
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schemes_path = os.path.join(current_dir, '..', '..', 'data', 'schemes.json')
    
    with open(schemes_path, 'r') as f:
        return json.load(f)

def match_schemes(user_profile: UserProfile, project_cost: float, business_category: str) -> List[SchemeMatchItem]:
    schemes = load_schemes()
    matches = []
    
    for scheme in schemes:
        eligibility = scheme.get('eligibility', {})
        reasons = []
        score = 100.0
        
        # Rule 1: Project Cost Cap
        max_cost = eligibility.get('max_project_cost')
        if max_cost and project_cost > max_cost:
            continue # Hard reject
            
        reasons.append(f"Project cost (₹{project_cost}) is within the scheme cap (₹{max_cost}).")
        
        # Rule 2: Interests / Category match
        required_interests = eligibility.get('required_interests', [])
        if required_interests:
            if business_category not in required_interests:
                continue # Hard reject
            reasons.append(f"Business category '{business_category}' is an eligible sector.")
            
        # Add subsidy reason if applicable
        subsidy = scheme.get('subsidy_percent', 0)
        if subsidy > 0:
            reasons.append(f"Provides {subsidy}% subsidy on project cost.")
            
        matches.append(SchemeMatchItem(
            scheme_name=scheme['scheme_name'],
            match_score=score,
            reasons=reasons,
            application_route=scheme['application_route'],
            official_source=scheme['application_route']
        ))
        
    # Sort by match score descending
    matches.sort(key=lambda x: x.match_score, reverse=True)
    return matches
