"""
End-to-End Persona Verification Test matching Section 30 of project.md.

Demo Scenario:
A rural entrepreneur:
- Handicraft skill
- ₹30,000 capital
- Workspace
- Limited market access

Flow:
1. Profile analyzed
2. Opportunity Engine ranks Handicraft with top fit score
3. Explainability shows why recommended and why not perfect
4. Capability Gap identifies Marketing + Capital as major gaps
5. Partner Finder locates nearby complementary partner (Ramesh Verma)
6. Geospatial engine computes local evidence coverage
"""

import pytest
from app.models.user import EntrepreneurProfile, LocationPoint
from app.models.common import RiskLevel
from app.engines.opportunity_engine import OpportunityEngine
from app.engines.capability_gap_engine import CapabilityGapEngine
from app.engines.partner_engine import PartnerEngine
from app.engines.geospatial_engine import GeospatialEngine
from app.data.business_catalog import get_business_by_id


def test_section_30_demo_persona():
    # 1. Smart Profile Setup
    persona = EntrepreneurProfile(
        user_id="demo_sih_lakshmi",
        name="Lakshmi Devi (Rural Artisan)",
        available_capital=30000.0,
        skills=["Handicraft", "Weaving", "Embroidery"],
        experience_years=3.0,
        resources=["Workspace", "Basic Wooden Loom"],
        interests=["handicraft_textiles"],
        location=LocationPoint(
            latitude=28.6140,
            longitude=77.2090,
            village_or_town="Kalyanpur Village",
            district="Central District",
            state="Demo State",
            service_radius_km=10.0
        ),
        risk_preference=RiskLevel.MEDIUM,
        has_market_connections=False,
        has_transport_access=False,
        has_digital_tools=False
    )

    # 2. Opportunity Discovery (Reverse Business Search)
    opp_search = OpportunityEngine.reverse_business_search(persona)
    assert opp_search.total_evaluated >= 5
    top_opp = opp_search.top_recommended
    assert top_opp.business_id == "handicraft_textiles"
    assert top_opp.overall_fit_score >= 70.0

    # 3. Explainability Rationale
    assert len(top_opp.why_recommended) >= 2
    assert any("skill" in r.lower() for r in top_opp.why_recommended)
    assert len(top_opp.why_not_perfect) >= 1
    assert any("distribution" in r.lower() or "capital" in r.lower() for r in top_opp.why_not_perfect)

    # 4. Capability Gap Detection
    gap_analysis = CapabilityGapEngine.evaluate_capabilities(persona)
    assert "Marketing" in gap_analysis.biggest_gaps or "Capital" in gap_analysis.biggest_gaps
    assert "Production" in gap_analysis.strongest_capabilities

    # 5. Partner Finder (Complementary matching)
    partner_cards = PartnerEngine.find_complementary_partners(persona, max_radius_km=25.0)
    assert len(partner_cards) >= 1
    top_partner = partner_cards[0]
    assert top_partner.partner_id == "partner_mkt_01"  # Ramesh Verma (Marketing + Capital)
    assert top_partner.synergy_score >= 80.0
    assert any("complementarity" in reason.lower() for reason in top_partner.why_matched)

    # 6. Local Evidence & Proximity Snapshot
    evidence_snapshot = GeospatialEngine.evaluate_local_signals(
        lat=persona.location.latitude,
        lon=persona.location.longitude,
        radius_km=persona.location.service_radius_km,
        category="handicraft_textiles"
    )
    assert evidence_snapshot.overall_evidence_coverage_percentage > 50.0
    assert evidence_snapshot.registered_enterprises_found >= 1
    assert len(evidence_snapshot.relevant_pois) >= 3
