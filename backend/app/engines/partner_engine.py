"""
Partner Matching, Complementarity Gap Analysis & Synergy Scoring Engine.
Implements the 6-Factor Synergy Formula and Privacy-Preserving Matching Flow.
(Section 6, 15, 25, 33 of project.md)
"""

from typing import List, Optional, Dict, Tuple
from ..models.user import EntrepreneurProfile
from ..models.partner import (
    PartnerProfile,
    PartnerSynergyResult,
    PartnerCard,
    SynergyFactorBreakdown,
    CapabilityGapAnalysis,
)
from ..models.common import VerificationState, CapabilityDimension
from ..config import settings, PartnerSynergyWeights
from ..data.sample_partners import SAMPLE_PARTNERS
from .geospatial_engine import GeospatialEngine
from .capability_gap_engine import CapabilityGapEngine


class PartnerEngine:
    """
    Deterministic Partner Matching & Synergy Scoring Engine.
    Matches one user's missing capabilities with another candidate's strengths.
    """

    @classmethod
    def calculate_skill_complementarity(
        cls,
        user_gaps: List[str],
        partner_capabilities: List[str],
        partner_skills: List[str]
    ) -> Tuple[float, List[str]]:
        """
        Evaluates how effectively candidate partner's strengths resolve the entrepreneur's capability gaps.
        """
        if not user_gaps:
            return 80.0, ["General operational synergy"]

        resolved_gaps = []
        partner_all = [c.lower() for c in partner_capabilities] + [s.lower() for s in partner_skills]

        for gap in user_gaps:
            gap_l = gap.lower()
            if any(gap_l in p or p in gap_l for p in partner_all):
                resolved_gaps.append(gap)

        if not resolved_gaps:
            # Check for partial matches
            if "marketing" in [g.lower() for g in user_gaps] and any("sales" in p or "market" in p for p in partner_all):
                resolved_gaps.append("Marketing")
            if "capital" in [g.lower() for g in user_gaps] and any("capital" in p or "invest" in p for p in partner_all):
                resolved_gaps.append("Capital")
            if "distribution" in [g.lower() for g in user_gaps] and any("transport" in p or "logistics" in p for p in partner_all):
                resolved_gaps.append("Distribution")

        match_ratio = len(resolved_gaps) / len(user_gaps)
        score = round(min(100.0, match_ratio * 80.0 + (20.0 if len(partner_capabilities) >= 2 else 10.0)), 1)
        return score, resolved_gaps

    @classmethod
    def calculate_capital_compatibility(
        cls,
        user_capital: float,
        partner_inv_min: float,
        partner_inv_max: float
    ) -> float:
        """
        Evaluates financial compatibility. If user has low capital (< ₹50k) and partner brings ₹1L+, high synergy.
        """
        if user_capital < 50000.0 and partner_inv_max >= 100000.0:
            return 95.0
        elif partner_inv_max >= user_capital:
            return 85.0
        elif partner_inv_max > 0:
            return 70.0
        else:
            return 50.0

    @classmethod
    def calculate_resource_complementarity(
        cls,
        user_resources: List[str],
        partner_resources: List[str]
    ) -> float:
        """
        Evaluates physical asset synergy (e.g. User has workspace + Partner has transport/tools).
        """
        if not partner_resources:
            return 45.0

        user_res_set = set(r.lower() for r in user_resources)
        partner_res_set = set(r.lower() for r in partner_resources)

        # Complementary if they bring distinct valuable assets
        overlap = user_res_set.intersection(partner_res_set)
        distinct = len(partner_resources) - len(overlap)

        score = 50.0 + min(45.0, distinct * 20.0)
        return min(100.0, round(score, 1))

    @classmethod
    def calculate_shared_interest(
        cls,
        user_interests: List[str],
        partner_interests: List[str]
    ) -> float:
        """
        Evaluates alignment in business categories.
        """
        if not user_interests or not partner_interests:
            return 60.0

        u_set = set(i.lower() for i in user_interests)
        p_set = set(i.lower() for i in partner_interests)

        if u_set.intersection(p_set):
            return 95.0
        elif any(any(u in p or p in u for p in p_set) for u in u_set):
            return 80.0
        else:
            return 40.0

    @classmethod
    def calculate_location_proximity_score(cls, distance_km: float, max_radius_km: float = 50.0) -> float:
        """
        Proximity decay curve.
        <= 5 km: 95-100, <= 15 km: 80-94, <= 30 km: 60-79, > 30 km: 30-59
        """
        if distance_km <= 5.0:
            return 95.0
        elif distance_km <= 15.0:
            return round(95.0 - (distance_km - 5.0) * 1.5, 1)
        elif distance_km <= max_radius_km:
            return round(max(30.0, 80.0 - (distance_km - 15.0) * 1.4), 1)
        else:
            return 20.0

    @classmethod
    def calculate_experience_compatibility(
        cls,
        user_exp: float,
        partner_exp: float
    ) -> float:
        """
        Evaluates experience compatibility.
        """
        combined = user_exp + partner_exp
        if combined >= 8.0:
            return 95.0
        elif combined >= 4.0:
            return 85.0
        else:
            return 70.0

    @classmethod
    def calculate_synergy(
        cls,
        profile: EntrepreneurProfile,
        partner: PartnerProfile,
        user_gap_analysis: Optional[CapabilityGapAnalysis] = None,
        weights: Optional[PartnerSynergyWeights] = None
    ) -> PartnerSynergyResult:
        """
        Calculates 6-factor partner synergy score.
        """
        w = weights or settings.DEFAULT_SYNERGY_WEIGHTS
        gaps = user_gap_analysis.biggest_gaps if user_gap_analysis else CapabilityGapEngine.evaluate_capabilities(profile).biggest_gaps

        # 1. Geodesic distance
        dist_km = GeospatialEngine.haversine_distance(
            profile.location.latitude,
            profile.location.longitude,
            partner.location.latitude,
            partner.location.longitude
        )

        # 2. Factor calculations
        skill_comp, resolved_gaps = cls.calculate_skill_complementarity(
            gaps, partner.capabilities, partner.skills
        )
        cap_comp = cls.calculate_capital_compatibility(
            profile.available_capital,
            partner.investment_min,
            partner.investment_max
        )
        res_comp = cls.calculate_resource_complementarity(
            profile.resources,
            partner.resources
        )
        shared_int = cls.calculate_shared_interest(
            profile.interests,
            partner.business_interests
        )
        loc_prox = cls.calculate_location_proximity_score(dist_km)
        exp_comp = cls.calculate_experience_compatibility(
            profile.experience_years,
            partner.experience_years
        )

        factors = SynergyFactorBreakdown(
            skill_complementarity=skill_comp,
            capital_compatibility=cap_comp,
            resource_complementarity=res_comp,
            shared_interest=shared_int,
            location_proximity=loc_prox,
            experience_compatibility=exp_comp
        )

        # 3. Weighted composite synergy score (Section 6 & 25)
        composite = round(
            w.skill_complementarity * skill_comp +
            w.capital_compatibility * cap_comp +
            w.resource_complementarity * res_comp +
            w.shared_interest * shared_int +
            w.location_proximity * loc_prox +
            w.experience_compatibility * exp_comp,
            1
        )
        synergy_score = max(0.0, min(100.0, composite))

        # 4. Positive match reasons
        match_reasons = []
        if skill_comp >= 75.0:
            match_reasons.append("✓ Skill complementarity (Fills key missing capabilities)")
        if cap_comp >= 80.0:
            match_reasons.append(f"✓ Capital compatibility (Can contribute ₹{partner.investment_min:,.0f} – ₹{partner.investment_max:,.0f})")
        if shared_int >= 80.0:
            match_reasons.append("✓ Shared business category interest")
        if loc_prox >= 75.0:
            match_reasons.append(f"✓ Geographic proximity (~{dist_km:.1f} km away)")
        if res_comp >= 70.0:
            match_reasons.append("✓ Resource complementarity (Brings operational assets)")

        unmet = [g for g in gaps if g not in resolved_gaps]

        return PartnerSynergyResult(
            partner_id=partner.partner_id,
            synergy_score=synergy_score,
            distance_km=dist_km,
            factor_breakdown=factors,
            match_reasons=match_reasons or ["✓ General micro-enterprise compatibility"],
            unmet_gaps=unmet
        )

    @classmethod
    def find_complementary_partners(
        cls,
        profile: EntrepreneurProfile,
        max_radius_km: float = 50.0,
        min_synergy_score: float = 50.0,
        partner_pool: Optional[List[PartnerProfile]] = None,
        weights: Optional[PartnerSynergyWeights] = None
    ) -> List[PartnerCard]:
        """
        Searches candidate partner database, evaluates synergy, and formats privacy-preserving partner cards.
        """
        pool = partner_pool or SAMPLE_PARTNERS
        gap_analysis = CapabilityGapEngine.evaluate_capabilities(profile)

        synergy_results: List[Tuple[PartnerProfile, PartnerSynergyResult]] = []

        for partner in pool:
            dist = GeospatialEngine.haversine_distance(
                profile.location.latitude,
                profile.location.longitude,
                partner.location.latitude,
                partner.location.longitude
            )
            if dist <= max_radius_km:
                syn_res = cls.calculate_synergy(profile, partner, gap_analysis, weights)
                if syn_res.synergy_score >= min_synergy_score:
                    synergy_results.append((partner, syn_res))

        # Sort by synergy score descending
        synergy_results.sort(key=lambda x: x[1].synergy_score, reverse=True)

        # Build Privacy-Preserving Partner Cards (Section 6, 15, 33)
        partner_cards: List[PartnerCard] = []
        for partner, syn in synergy_results:
            area_str = f"Within {syn.distance_km:.1f} km ({partner.location.village_or_town or partner.location.district})"
            inv_str = f"₹{partner.investment_min:,.0f} – ₹{partner.investment_max:,.0f}"
            strengths = partner.capabilities if partner.capabilities else partner.skills

            title = f"Partner ({', '.join(strengths[:2]) or 'Business Collaborator'})"

            card = PartnerCard(
                partner_id=partner.partner_id,
                display_title=title,
                approximate_area=area_str,
                distance_km=syn.distance_km,
                key_strengths=strengths,
                investment_range_str=inv_str,
                shared_interests=partner.business_interests,
                synergy_score=syn.synergy_score,
                verification_state=partner.verification_state,
                why_matched=syn.match_reasons,
                is_contact_shared=False,
                contact_phone=None
            )
            partner_cards.append(card)

        return partner_cards

    @classmethod
    def reveal_partner_contact(
        cls,
        partner_id: str,
        partner_pool: Optional[List[PartnerProfile]] = None
    ) -> Optional[Dict[str, str]]:
        """
        Mutual consent flow (Section 6, 33).
        Exposes contact phone only upon confirmed mutual interest.
        """
        pool = partner_pool or SAMPLE_PARTNERS
        for p in pool:
            if p.partner_id == partner_id:
                return {
                    "partner_id": p.partner_id,
                    "name": p.name,
                    "phone": p.phone or "Not provided",
                    "verification_state": p.verification_state.value,
                    "consent_status": "MUTUAL_CONSENT_GRANTED"
                }
        return None
