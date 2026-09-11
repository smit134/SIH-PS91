"""
Capability Gap Detection Engine.
Evaluates 6 Core Capability Dimensions: Production, Capital, Marketing, Distribution, Technology, Management.
Identifies strengths and biggest capability gaps. (Section 6 & 15 of project.md)
"""

from typing import Dict, List, Tuple
from ..models.user import EntrepreneurProfile
from ..models.partner import CapabilityGapAnalysis
from ..models.common import CapabilityDimension


class CapabilityGapEngine:
    """
    Deterministic Capability Gap Evaluator.
    Analyzes an entrepreneur's profile across 6 key business pillars.
    """

    @classmethod
    def evaluate_capabilities(cls, profile: EntrepreneurProfile) -> CapabilityGapAnalysis:
        """
        Calculates scores (0-100) for all 6 dimensions and ranks strengths vs gaps.
        """
        scores: Dict[CapabilityDimension, float] = {}

        # 1. Production Dimension: Technical skills, years of experience, owned production tools
        has_craft_or_agri_skills = len(profile.skills) > 0
        skill_count_factor = min(40.0, len(profile.skills) * 15.0)
        exp_factor = min(30.0, profile.experience_years * 10.0)
        tools_factor = 25.0 if any(r.lower() in ["tools", "workspace", "sewing machines", "land", "shed"] for r in profile.resources) else 10.0
        production_score = round(min(100.0, 15.0 + skill_count_factor + exp_factor + tools_factor), 1)
        scores[CapabilityDimension.PRODUCTION] = production_score

        # 2. Capital Dimension: Available capital vs typical baseline (₹1,50,000)
        # ₹20k -> ~35%, ₹30k -> ~44%, ₹80k -> ~75%, ₹1.5L+ -> 95-100%
        cap = profile.available_capital
        if cap <= 10000:
            capital_score = 25.0
        elif cap <= 30000:
            capital_score = round(25.0 + (cap - 10000) * (20.0 / 20000), 1)  # 25-45%
        elif cap <= 100000:
            capital_score = round(45.0 + (cap - 30000) * (35.0 / 70000), 1)  # 45-80%
        else:
            capital_score = round(min(100.0, 80.0 + (cap - 100000) * (20.0 / 100000)), 1)
        scores[CapabilityDimension.CAPITAL] = capital_score

        # 3. Marketing Dimension: Established market connections, digital commerce, sales skills
        marketing_score = 20.0
        if profile.has_market_connections:
            marketing_score += 45.0
        if any("market" in s.lower() or "sales" in s.lower() for s in profile.skills):
            marketing_score += 25.0
        if profile.has_digital_tools:
            marketing_score += 10.0
        scores[CapabilityDimension.MARKETING] = round(min(100.0, marketing_score), 1)

        # 4. Distribution Dimension: Transport access, logistics, distribution skills
        dist_score = 25.0
        if profile.has_transport_access or any("transport" in r.lower() or "van" in r.lower() or "tractor" in r.lower() for r in profile.resources):
            dist_score += 50.0
        if any("distribution" in s.lower() or "logistics" in s.lower() for s in profile.skills):
            dist_score += 20.0
        scores[CapabilityDimension.DISTRIBUTION] = round(min(100.0, dist_score), 1)

        # 5. Technology Dimension: Modern equipment, digital tools, power/machinery
        tech_score = 30.0
        if profile.has_digital_tools:
            tech_score += 25.0
        if any("machine" in r.lower() or "equipment" in r.lower() or "power" in r.lower() for r in profile.resources):
            tech_score += 30.0
        scores[CapabilityDimension.TECHNOLOGY] = round(min(100.0, tech_score), 1)

        # 6. Management Dimension: Experience, record keeping, planning
        mgmt_score = 40.0 + min(35.0, profile.experience_years * 8.0)
        if any("management" in s.lower() or "accounting" in s.lower() for s in profile.skills):
            mgmt_score += 20.0
        scores[CapabilityDimension.MANAGEMENT] = round(min(100.0, mgmt_score), 1)

        # Identify strengths vs gaps
        sorted_dims = sorted(scores.items(), key=lambda x: x[1])
        biggest_gaps = [dim.value for dim, score in sorted_dims if score < 60.0]
        if not biggest_gaps:
            biggest_gaps = [sorted_dims[0][0].value, sorted_dims[1][0].value]

        strongest = [dim.value for dim, score in reversed(sorted_dims) if score >= 60.0]
        if not strongest:
            strongest = [sorted_dims[-1][0].value, sorted_dims[-2][0].value]

        narrative = (
            f"Strongest standing in {', '.join(strongest[:2])}. "
            f"Key capability gaps detected in {', '.join(biggest_gaps[:2])}."
        )

        return CapabilityGapAnalysis(
            dimension_scores=scores,
            biggest_gaps=biggest_gaps,
            strongest_capabilities=strongest,
            summary=narrative
        )
