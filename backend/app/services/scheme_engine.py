import json
import os
from typing import List, Optional
from app.models.financials import UserProfile, SchemeMatchItem

def load_schemes() -> List[dict]:
    """Loads schemes catalog from backend/data/schemes.json."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schemes_path = os.path.join(current_dir, '..', '..', 'data', 'schemes.json')
    
    with open(schemes_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_subsidy_amount(scheme: dict, project_cost: float) -> float:
    """Calculates realistic subsidy amount based on scheme subsidy percent and project cost."""
    subsidy_pct = float(scheme.get('subsidy_percent', 0.0))
    if subsidy_pct <= 0:
        return 0.0
    
    calculated = project_cost * (subsidy_pct / 100.0)
    
    # Cap specific schemes according to official guidelines
    short_code = scheme.get('short_code', '')
    if short_code == 'PMFME':
        # PMFME 35% grant capped at ₹10 Lakhs
        return min(calculated, 1000000.0)
    elif short_code == 'NLM':
        # NLM 50% subsidy capped at ₹25-50 Lakhs
        return min(calculated, 2500000.0)
    elif short_code == 'ACABC':
        # ACABC 44% on up to 20L max project
        return min(calculated, 880000.0)
    elif short_code == 'SAMARTH':
        return min(calculated, 25000.0)
    
    return round(calculated, 2)


def match_schemes(
    user_profile: Optional[UserProfile] = None, 
    project_cost: float = 150000.0, 
    business_category: str = "all"
) -> List[SchemeMatchItem]:
    """
    Evaluates, personalizes, and scores government schemes according to:
    1. Business opportunity / sector alignment
    2. Project cost & capex leverage
    3. User profile information (capital/equity, vocational skills, rural location, collateral)
    """
    schemes = load_schemes()
    matches: List[SchemeMatchItem] = []
    
    norm_cat = (business_category or "").strip().lower()
    user_capital = float(user_profile.capital) if user_profile and user_profile.capital else None
    user_skills = [s.lower() for s in (user_profile.skills if user_profile else [])]
    user_interests = [i.lower() for i in (user_profile.interests if user_profile else [])]
    user_resources = [r.lower() for r in (user_profile.resources if user_profile else [])]
    user_location = user_profile.location if user_profile else {}
    
    # Check if user profile has inferred indicators
    is_rural_cluster = True  # Default true in ThinkForge rural context
    district = user_location.get("district", "Wardha") if isinstance(user_location, dict) else "Wardha"

    for scheme in schemes:
        eligibility = scheme.get('eligibility', {})
        applicable_opps = [o.lower() for o in scheme.get('applicable_opportunities', [])]
        reasons = []
        user_specific_reasons = []
        score = 78.0
        
        # Rule 1: Project Cost Cap
        max_cost = float(eligibility.get('max_project_cost') or scheme.get('project_cap') or 1e9)
        if project_cost > max_cost:
            continue  # Exceeds maximum eligible project cost
            
        reasons.append(f"Project cost (₹{int(project_cost):,}) is within scheme limit (₹{int(max_cost):,}).")
        
        # Rule 2: Opportunity & Sector Relevance
        is_direct_match = False
        if norm_cat and norm_cat != "all":
            if norm_cat in applicable_opps:
                is_direct_match = True
                reasons.append(f"Direct policy match: Program created for {business_category.replace('_', ' ').title()}.")
            else:
                req_interests = [i.lower() for i in eligibility.get('required_interests', [])]
                if any(kw in norm_cat for kw in ["food", "spice", "agro"]) and any(i in ["food processing", "agro-processing", "spices"] for i in req_interests):
                    is_direct_match = True
                elif any(kw in norm_cat for kw in ["dairy", "cattle", "milk"]) and any("dairy" in i or "livestock" in i for i in req_interests):
                    is_direct_match = True
                elif any(kw in norm_cat for kw in ["vermicompost", "organic", "bio"]) and any("organic" in i or "vermicompost" in i for i in req_interests):
                    is_direct_match = True
                elif any(kw in norm_cat for kw in ["tailor", "garment", "apparel"]) and any("tailoring" in i or "garments" in i for i in req_interests):
                    is_direct_match = True
                elif any(kw in norm_cat for kw in ["handicraft", "craft", "textile"]) and any("handicraft" in i or "textiles" in i for i in req_interests):
                    is_direct_match = True
                
                if is_direct_match:
                    reasons.append(f"Sector match: Aligns with {scheme.get('nodal_agency')}.")
                elif req_interests and not applicable_opps:
                    continue  # Incompatible sector requirement
        
        if is_direct_match:
            score += 12.0

        # Rule 3: Personalization based on User's Information
        if user_capital is not None:
            # Check promoter contribution required (typically 5% - 15% of project cost)
            required_margin = project_cost * 0.10
            if user_capital >= required_margin:
                user_specific_reasons.append(f"Your available equity (₹{int(user_capital):,}) satisfies the 10% promoter margin.")
                score += 4.0
            elif scheme.get('collateral_free', False):
                user_specific_reasons.append("Low capital requirement: Fits within institutional credit limits.")
                score += 3.0

        if user_skills:
            matched_skill = False
            for s in user_skills:
                if any(s in opp for opp in applicable_opps) or any(s in req.lower() for req in eligibility.get('required_interests', [])):
                    matched_skill = True
                    break
                # Common skill keyword checks
                if "dairy" in s and scheme.get("short_code") in ["NLM", "PMFME"]:
                    matched_skill = True
                elif ("food" in s or "agro" in s or "agri" in s) and scheme.get("short_code") in ["PMFME", "PMEGP"]:
                    matched_skill = True
                elif ("soil" in s or "compost" in s or "organic" in s) and scheme.get("short_code") in ["PKVY", "ACABC"]:
                    matched_skill = True
                elif ("tailor" in s or "stitch" in s or "textile" in s) and scheme.get("short_code") in ["SAMARTH", "SFURTI"]:
                    matched_skill = True
                elif ("craft" in s or "weav" in s) and scheme.get("short_code") in ["SFURTI", "PMEGP"]:
                    matched_skill = True

            if matched_skill:
                user_specific_reasons.append(f"Your primary skills directly fulfill the technical qualification criteria.")
                score += 4.0

        if user_interests:
            if any(any(i in opp for opp in applicable_opps) for i in user_interests):
                user_specific_reasons.append("Matches your stated sector preference from your profile.")
                score += 2.0

        # Rural location bonus (e.g. 35% PMEGP rural subsidy)
        if is_rural_cluster and scheme.get('short_code') == 'PMEGP':
            user_specific_reasons.append(f"Rural enterprise location in {district} unlocks the top 35% subsidy rate (vs 25% urban).")
            score += 3.0
        elif scheme.get('short_code') == 'PMFME':
            user_specific_reasons.append(f"Aligned with {district} One-District-One-Product (ODOP) focus.")
            score += 2.0

        # Subsidy and collateral benefits
        subsidy_pct = float(scheme.get('subsidy_percent', 0.0))
        if subsidy_pct >= 35.0:
            score += 3.0
            reasons.append(f"High-impact subsidy offering: {scheme.get('subsidy_rate_text', f'{subsidy_pct}% subsidy')}.")
        elif subsidy_pct > 0:
            score += 1.5
            reasons.append(f"Credit-linked subsidy assistance: {scheme.get('subsidy_rate_text', f'{subsidy_pct}% subsidy')}.")
        
        if scheme.get('collateral_free', False):
            reasons.append("100% collateral-free institutional credit under government guarantee cover.")
            
        estimated_subsidy = calculate_subsidy_amount(scheme, project_cost)
        if estimated_subsidy > 0:
            reasons.append(f"Estimated financial assistance: ~₹{int(estimated_subsidy):,} on your project investment.")

        # Combine reasons with user-specific reasons prioritized at top
        combined_reasons = user_specific_reasons + reasons

        matches.append(SchemeMatchItem(
            scheme_id=scheme.get('scheme_id'),
            scheme_name=scheme['scheme_name'],
            short_code=scheme.get('short_code'),
            nodal_agency=scheme.get('nodal_agency'),
            match_score=min(99.0, round(score, 1)),
            reasons=combined_reasons,
            subsidy_percent=subsidy_pct,
            subsidy_rate_text=scheme.get('subsidy_rate_text'),
            max_project_cost=max_cost,
            estimated_subsidy_amount=estimated_subsidy,
            applicable_opportunities=scheme.get('applicable_opportunities', []),
            priority_category=scheme.get('priority_category'),
            collateral_free=scheme.get('collateral_free', False),
            description=scheme.get('description'),
            status_tag=scheme.get('status_tag'),
            documents_required=scheme.get('documents_required', []),
            application_route=scheme['application_route'],
            official_source=scheme.get('official_source', scheme['application_route'])
        ))
        
    # Sort by match score descending
    matches.sort(key=lambda x: x.match_score, reverse=True)
    return matches


def get_all_schemes() -> List[dict]:
    """Returns raw scheme catalog."""
    return load_schemes()
