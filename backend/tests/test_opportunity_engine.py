"""
Unit tests for Opportunity Scoring Engine, Reverse Business Search, Explainability, and Comparison.
"""

import pytest
from app.models.user import EntrepreneurProfile, LocationPoint
from app.models.common import RiskLevel, EvidenceClass
from app.engines.opportunity_engine import OpportunityEngine
from app.data.business_catalog import get_business_by_id, get_all_businesses


@pytest.fixture
def handicraft_user() -> EntrepreneurProfile:
    return EntrepreneurProfile(
        user_id="artisan_01",
        name="Lakshmi Devi",
        available_capital=30000.0,
        skills=["Handicraft", "Weaving", "Embroidery"],
        experience_years=3.0,
        resources=["Workspace", "Basic Tools"],
        interests=["Handicraft & Textile Products"],
        location=LocationPoint(latitude=28.6140, longitude=77.2090, service_radius_km=10.0),
        risk_preference=RiskLevel.MEDIUM,
        has_transport_access=False,
        has_market_connections=False,
        has_digital_tools=False
    )


def test_handicraft_scoring_high_fit(handicraft_user):
    handicraft_biz = get_business_by_id("handicraft_textiles")
    assert handicraft_biz is not None

    result = OpportunityEngine.score_business(handicraft_user, handicraft_biz)

    # Lakshmi has strong handicraft skills, adequate min capital, and workspace
    assert result.overall_fit_score >= 70.0
    assert result.factor_breakdown.skill_fit >= 80.0
    assert result.factor_breakdown.capital_fit >= 70.0
    assert len(result.why_recommended) > 0
    assert result.evidence_class == EvidenceClass.DERIVED


def test_dairy_scoring_low_fit_due_to_capital_and_skills(handicraft_user):
    dairy_biz = get_business_by_id("dairy_micro_farm")
    assert dairy_biz is not None

    result = OpportunityEngine.score_business(handicraft_user, dairy_biz)

    # Min capital for dairy is ₹1.5L (Lakshmi has ₹30k), and she lacks cattle skills
    assert result.overall_fit_score < result.factor_breakdown.skill_fit or result.overall_fit_score < 65.0
    assert result.factor_breakdown.capital_fit <= 30.0
    assert result.why_not_this_business is not None
    assert any("Capital requirement" in r for r in result.why_not_this_business)


def test_reverse_business_search(handicraft_user):
    res = OpportunityEngine.reverse_business_search(handicraft_user)

    assert res.total_evaluated == len(get_all_businesses())
    assert len(res.ranked_opportunities) > 0
    # Top ranked should be handicraft or tailoring
    top_id = res.top_recommended.business_id
    assert top_id in ["handicraft_textiles", "garment_tailoring_unit"]


def test_business_comparison(handicraft_user):
    comparison = OpportunityEngine.compare_businesses(
        handicraft_user,
        ["handicraft_textiles", "dairy_micro_farm", "food_processing_spices"]
    )

    assert len(comparison.businesses) == 3
    assert len(comparison.comparison_table) >= 5
    assert comparison.highest_fit_business_id == "handicraft_textiles"
