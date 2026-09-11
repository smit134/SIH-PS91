"""
Unit tests for Capability Gap Detection Engine.
"""

import pytest
from app.models.user import EntrepreneurProfile, LocationPoint
from app.models.common import RiskLevel, CapabilityDimension
from app.engines.capability_gap_engine import CapabilityGapEngine


def test_capability_gap_detection():
    # User with strong production skill, but low capital and no market access
    user = EntrepreneurProfile(
        user_id="user_gap_test",
        available_capital=20000.0,
        skills=["Handicraft", "Weaving"],
        experience_years=4.0,
        resources=["Workspace"],
        location=LocationPoint(latitude=28.6140, longitude=77.2090),
        risk_preference=RiskLevel.MEDIUM,
        has_market_connections=False,
        has_transport_access=False
    )

    analysis = CapabilityGapEngine.evaluate_capabilities(user)

    # Production should be high
    assert analysis.dimension_scores[CapabilityDimension.PRODUCTION] >= 70.0
    
    # Capital, Marketing, and Distribution should be identified as gaps
    assert "Marketing" in analysis.biggest_gaps or "Capital" in analysis.biggest_gaps
    assert analysis.dimension_scores[CapabilityDimension.MARKETING] < 50.0
    assert analysis.dimension_scores[CapabilityDimension.CAPITAL] < 50.0
