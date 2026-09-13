"""
Opportunity Scoring, Reverse Business Search, Explainability, and Comparison Engine.
Implements the 7-Factor Fit Scoring Formula and transparent explainability logic.
(Section 7, 8, 13, 24 of project.md)
"""

from typing import List, Dict, Optional, Tuple
from ..models.user import EntrepreneurProfile
from ..models.business import (
    BusinessCategory,
    BusinessFitResult,
    BusinessComparisonResult,
    FactorBreakdown,
    ReverseSearchResult,
)
from ..models.common import RiskLevel, EvidenceClass
from ..config import settings, OpportunityScoringWeights
from sqlalchemy.ext.asyncio import AsyncSession
from ..data.business_catalog import get_all_businesses, get_business_by_id
from .geospatial_engine import GeospatialEngine


class OpportunityEngine:
    """
    Deterministic Opportunity Scoring & Explainability Engine.
    Combines user profile capabilities, business requirements, and hyper-local signals.
    """

    @classmethod
    def calculate_capital_fit(cls, available_capital: float, min_req: float, rec_req: float) -> float:
        """
        Evaluates capital adequacy (0-100).
        """
        if available_capital >= rec_req:
            return 100.0
        elif available_capital >= min_req:
            # Linear interpolation between min and recommended (70 to 95)
            ratio = (available_capital - min_req) / max(1.0, rec_req - min_req)
            return round(70.0 + ratio * 25.0, 1)
        else:
            # Below minimum startup capital requirement
            ratio = available_capital / max(1.0, min_req)
            return round(max(10.0, ratio * 60.0), 1)

    @classmethod
    def calculate_skill_fit(cls, user_skills: List[str], required_skills: List[str], optional_skills: List[str]) -> Tuple[float, List[str], List[str]]:
        """
        Evaluates skill match percentage and identifies matched vs missing skills.
        """
        if not required_skills:
            return 100.0, [], []

        user_skills_lower = [s.strip().lower() for s in user_skills]
        matched_required = []
        missing_required = []

        for req in required_skills:
            req_l = req.strip().lower()
            if any(req_l in u or u in req_l for u in user_skills_lower):
                matched_required.append(req)
            else:
                missing_required.append(req)

        matched_optional = []
        for opt in optional_skills:
            opt_l = opt.strip().lower()
            if any(opt_l in u or u in opt_l for u in user_skills_lower):
                matched_optional.append(opt)

        match_ratio = len(matched_required) / len(required_skills)
        base_score = match_ratio * 85.0
        opt_bonus = min(15.0, len(matched_optional) * 7.5)
        skill_score = round(min(100.0, base_score + opt_bonus), 1)

        # Baseline floor if user has generic manual/agri skill
        if skill_score < 30.0 and len(user_skills) > 0:
            skill_score = 35.0

        return skill_score, matched_required, missing_required

    @classmethod
    def calculate_resource_fit(cls, user_resources: List[str], required_resources: List[str]) -> Tuple[float, List[str], List[str]]:
        """
        Evaluates physical resource match.
        """
        if not required_resources:
            return 100.0, [], []

        user_res_lower = [r.strip().lower() for r in user_resources]
        matched = []
        missing = []

        for req in required_resources:
            req_l = req.strip().lower()
            if any(req_l in u or u in req_l for u in user_res_lower):
                matched.append(req)
            else:
                missing.append(req)

        match_ratio = len(matched) / len(required_resources)
        score = round(match_ratio * 90.0 + (10.0 if len(user_resources) > 0 else 0.0), 1)
        return min(100.0, max(20.0, score)), matched, missing

    @classmethod
    def calculate_market_access(cls, profile: EntrepreneurProfile, local_signal: float) -> float:
        """
        Evaluates market accessibility based on direct connections, transport, and local signal.
        """
        base = 40.0
        if profile.has_market_connections:
            base += 35.0
        if profile.has_transport_access or any("transport" in r.lower() or "van" in r.lower() for r in profile.resources):
            base += 15.0
        if profile.has_digital_tools:
            base += 10.0
        score = round(0.7 * base + 0.3 * local_signal, 1)
        return min(100.0, score)

    @classmethod
    def calculate_margin_potential(cls, margin_pct: float) -> float:
        """
        Normalizes gross margin percentage to a 0-100 score.
        20% -> 60, 35% -> 80, 50%+ -> 95-100
        """
        normalized = min(100.0, margin_pct * 2.0)
        return round(max(30.0, normalized), 1)

    @classmethod
    def calculate_risk_suitability(cls, user_risk: RiskLevel, business_risk: RiskLevel) -> float:
        """
        Evaluates suitability of business risk relative to entrepreneur's tolerance.
        """
        risk_map = {RiskLevel.LOW: 1, RiskLevel.MEDIUM: 2, RiskLevel.HIGH: 3}
        u_val = risk_map.get(user_risk, 2)
        b_val = risk_map.get(business_risk, 2)

        if u_val >= b_val:
            return 95.0
        elif u_val == 1 and b_val == 2:
            return 70.0
        elif u_val == 2 and b_val == 3:
            return 65.0
        else:
            return 45.0

    @classmethod
    async def score_business(
        cls,
        session: AsyncSession,
        profile: EntrepreneurProfile,
        business: BusinessCategory,
        weights: Optional[OpportunityScoringWeights] = None
    ) -> BusinessFitResult:
        """
        Scores a single business category against the entrepreneur profile and hyper-local evidence.
        Produces full factor breakdown and explainability rationale.
        """
        w = weights or settings.DEFAULT_OPPORTUNITY_WEIGHTS

        # 1. Hyper-local signal
        local_snapshot = await GeospatialEngine.evaluate_local_signals(
            session=session,
            lat=profile.location.latitude,
            lon=profile.location.longitude,
            radius_km=profile.location.service_radius_km,
            category=business.id
        )
        local_opp_score = local_snapshot.local_opportunity_composite

        # 2. Factor calculations
        cap_fit = cls.calculate_capital_fit(
            profile.available_capital,
            business.requirements.min_capital_required,
            business.requirements.recommended_capital
        )
        skill_fit, matched_skills, missing_skills = cls.calculate_skill_fit(
            profile.skills,
            business.requirements.required_skills,
            business.requirements.optional_skills
        )
        res_fit, matched_res, missing_res = cls.calculate_resource_fit(
            profile.resources,
            business.requirements.required_resources
        )
        mkt_access = cls.calculate_market_access(profile, local_opp_score)
        margin_score = cls.calculate_margin_potential(business.requirements.typical_margin_percentage)
        risk_suit = cls.calculate_risk_suitability(profile.risk_preference, business.requirements.inherent_risk)

        factors = FactorBreakdown(
            capital_fit=cap_fit,
            skill_fit=skill_fit,
            resource_fit=res_fit,
            local_opportunity=local_opp_score,
            market_access=mkt_access,
            margin_potential=margin_score,
            risk_suitability=risk_suit
        )

        # 3. Weighted composite fit score (Section 24)
        composite_score = round(
            w.capital_fit * cap_fit +
            w.skill_fit * skill_fit +
            w.resource_fit * res_fit +
            w.local_opportunity * local_opp_score +
            w.market_access * mkt_access +
            w.margin_potential * margin_score +
            w.risk_suitability * risk_suit,
            1
        )
        
        # Interest match bonus
        interest_bonus = 0.0
        matched_interests = []
        if profile.interests:
            b_sector = business.sector.lower()
            b_name = business.name.lower()
            b_tags = [t.lower() for t in business.tags]
            
            for ui in profile.interests:
                if not ui: continue
                ui_words = [w for w in ui.lower().replace('&', ' ').replace('-', ' ').split() if len(w) > 3]
                
                for word in ui_words:
                    if word in b_sector or word in b_name or any(word in t for t in b_tags):
                        interest_bonus += 15.0
                        matched_interests.append(ui)
                        break

        overall_fit = max(0.0, min(100.0, composite_score + interest_bonus))

        # 4. Explainability Generation (Section 8)
        why_recommended = []
        why_not_perfect = []
        why_not_this_business = []

        if matched_interests:
            why_recommended.append(f"Direct match with your stated interest: {matched_interests[0]}.")
        if skill_fit >= 75.0:
            why_recommended.append(f"Strong skill alignment: {', '.join(matched_skills[:2]) or 'Direct artisanal skills'} already available.")
        if cap_fit >= 80.0:
            why_recommended.append(f"Available capital (₹{profile.available_capital:,.0f}) comfortably meets minimum startup requirement.")
        elif cap_fit >= 60.0:
            why_recommended.append(f"Capital is within viable range (min requirement: ₹{business.requirements.min_capital_required:,.0f}).")
        if res_fit >= 70.0:
            why_recommended.append(f"Required physical resources ({', '.join(matched_res[:2]) or 'Workspace'}) are largely accessible.")
        if local_opp_score >= 75.0:
            why_recommended.append("Local market opportunity signal is favorable within selected radius.")
        if margin_score >= 80.0:
            why_recommended.append(f"Attractive typical gross margin profile (~{business.requirements.typical_margin_percentage:.1f}%).")

        # Why not perfect
        if missing_skills:
            why_not_perfect.append(f"Missing specific secondary skills: {', '.join(missing_skills[:2])}.")
        if cap_fit < 85.0:
            why_not_perfect.append(f"Capital is below recommended scale of ₹{business.requirements.recommended_capital:,.0f} (working capital cushion recommended).")
        if not profile.has_market_connections:
            why_not_perfect.append("Direct village/retail distribution channels need to be established.")
        if local_snapshot.overall_evidence_coverage_percentage < 75.0:
            why_not_perfect.append("Village-level demand relies on sub-district proxies rather than direct household censuses.")

        # Why NOT this business (Rejection reasons for low fit < 60)
        if overall_fit < 60.0 or cap_fit < 50.0 or skill_fit < 50.0:
            if cap_fit < 50.0:
                why_not_this_business.append(
                    f"Capital requirement (min ₹{business.requirements.min_capital_required:,.0f}) significantly exceeds available budget (₹{profile.available_capital:,.0f})."
                )
            if skill_fit < 50.0:
                why_not_this_business.append(
                    f"User lacks required technical domain skills ({', '.join(business.requirements.required_skills)})."
                )
            if local_snapshot.registered_enterprises_found >= 4:
                why_not_this_business.append("Local registered competitor density is high in this category.")

        estimated_profit = business.requirements.estimated_monthly_revenue - business.requirements.estimated_monthly_operating_cost

        return BusinessFitResult(
            business_id=business.id,
            business_name=business.name,
            sector=business.sector,
            overall_fit_score=overall_fit,
            evidence_confidence_score=local_snapshot.overall_evidence_coverage_percentage,
            evidence_class=EvidenceClass.DERIVED,
            factor_breakdown=factors,
            capital_required_min=business.requirements.min_capital_required,
            capital_required_rec=business.requirements.recommended_capital,
            estimated_monthly_profit=estimated_profit,
            estimated_break_even_months=business.requirements.break_even_months_estimate,
            inherent_risk=business.requirements.inherent_risk,
            why_recommended=why_recommended or ["General rural feasibility match."],
            why_not_perfect=why_not_perfect,
            why_not_this_business=why_not_this_business if why_not_this_business else None,
            confidence_limitations=[item.limitation_note for item in local_snapshot.coverage_breakdown if item.evidence_class != EvidenceClass.VERIFIED]
        )

    @classmethod
    async def reverse_business_search(
        cls,
        session: AsyncSession,
        profile: EntrepreneurProfile,
        weights: Optional[OpportunityScoringWeights] = None
    ) -> ReverseSearchResult:
        """
        USP #2: Resource -> Business Engine.
        'What can I start with what I already have?'
        Scores all businesses against entrepreneur resources & skills, ranking top matches.
        """
        all_businesses = get_all_businesses()
        scored_results: List[BusinessFitResult] = []

        for b in all_businesses:
            res = await cls.score_business(session, profile, b, weights)
            scored_results.append(res)

        scored_results.sort(key=lambda x: x.overall_fit_score, reverse=True)
        
        # --- AI PERSONALIZATION LAYER ---
        from sqlalchemy import select
        from ..models.interaction import UserInteraction
        
        interactions = []
        try:
            uid_str = profile.user_id
            stmt = select(UserInteraction).where(UserInteraction.user_id == uid_str)
            result = await session.execute(stmt)
            interactions = result.scalars().all()
        except Exception as e:
            print(f"Error fetching interactions: {e}")
            
        if interactions:
            from ..services.llm_service import personalize_recommendations
            top_candidates = scored_results[:10]  # Only send top 10 to LLM to save context
            ranked_top = await personalize_recommendations(profile, interactions, top_candidates)
            
            # Reconstruct the full list: ranked AI results first, then the rest
            scored_results = ranked_top + [r for r in scored_results if r not in ranked_top]

        top_rec = scored_results[0] if scored_results else None

        return ReverseSearchResult(
            total_evaluated=len(all_businesses),
            ranked_opportunities=scored_results,
            top_recommended=top_rec,
            available_resource_summary=profile.resources if profile.resources else ["None declared"],
            identified_skill_strengths=profile.skills if profile.skills else ["General labor"]
        )

    @classmethod
    async def compare_businesses(
        cls,
        session: AsyncSession,
        profile: EntrepreneurProfile,
        business_ids: List[str]
    ) -> BusinessComparisonResult:
        """
        Side-by-Side Business Comparison Matrix (Section 13).
        """
        results: List[BusinessFitResult] = []
        for bid in business_ids:
            biz = get_business_by_id(bid)
            if biz:
                results.append(await cls.score_business(session, profile, biz))

        if not results:
            # Fallback to top 3 from catalog
            reverse_results = await cls.reverse_business_search(session, profile)
            results = reverse_results.ranked_opportunities[:3]

        # Build comparison table
        table_rows = []
        headers = ["Fit Score", "Capital Required", "Risk", "Local Opportunity", "Skill Fit", "Break-even"]
        
        for h in headers:
            row_dict = {"Metric": h}
            for res in results:
                if h == "Fit Score":
                    row_dict[res.business_name] = f"{res.overall_fit_score:.0f}/100"
                elif h == "Capital Required":
                    row_dict[res.business_name] = f"₹{res.capital_required_rec/100000:.1f}L"
                elif h == "Risk":
                    row_dict[res.business_name] = res.inherent_risk.value
                elif h == "Local Opportunity":
                    row_dict[res.business_name] = f"{res.factor_breakdown.local_opportunity:.0f}/100"
                elif h == "Skill Fit":
                    row_dict[res.business_name] = f"{res.factor_breakdown.skill_fit:.0f}%"
                elif h == "Break-even":
                    row_dict[res.business_name] = f"{res.estimated_break_even_months} months"
            table_rows.append(row_dict)

        highest_fit = max(results, key=lambda x: x.overall_fit_score).business_id
        lowest_risk = min(results, key=lambda x: 1 if x.inherent_risk == RiskLevel.LOW else (2 if x.inherent_risk == RiskLevel.MEDIUM else 3)).business_id
        fastest_breakeven = min(results, key=lambda x: x.estimated_break_even_months).business_id

        return BusinessComparisonResult(
            businesses=results,
            comparison_table=table_rows,
            highest_fit_business_id=highest_fit,
            lowest_risk_business_id=lowest_risk,
            fastest_breakeven_business_id=fastest_breakeven
        )
