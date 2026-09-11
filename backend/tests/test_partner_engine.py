"""
Unit tests for Partner Synergy & Matchmaking Engine.
"""

import pytest
from app.models.user import EntrepreneurProfile, LocationPoint
from app.models.partner import PartnerProfile
from app.models.common import RiskLevel, VerificationState
from app.engines.partner_engine import PartnerEngine
from app.data.sample_partners import SAMPLE_PARTNERS


def test_complementary_partner_synergy():
    # Artisan User
    artisan = EntrepreneurProfile(
        user_id="artisan_Lakshmi",
        name="Lakshmi",
        available_capital=30000.0,
        skills=["Handicraft", "Textile Design"],
        experience_years=3.0,
        resources=["Workspace"],
        interests=["handicraft_textiles"],
        location=LocationPoint(latitude=28.6140, longitude=77.2090),
        risk_preference=RiskLevel.MEDIUM,
        has_market_connections=False,
        has_transport_access=False
    )

    partner_cards = PartnerEngine.find_complementary_partners(artisan, max_radius_km=30.0)

    assert len(partner_cards) > 0
    top_partner = partner_cards[0]
    
    # Top partner should have high synergy (> 75)
    assert top_partner.synergy_score >= 75.0
    # Must preserve privacy before consent
    assert top_partner.is_contact_shared is False
    assert top_partner.contact_phone is None
    assert "Within" in top_partner.approximate_area
    assert len(top_partner.why_matched) > 0


def test_mutual_consent_contact_reveal():
    contact_data = PartnerEngine.reveal_partner_contact("partner_mkt_01")
    assert contact_data is not None
    assert contact_data["partner_id"] == "partner_mkt_01"
    assert contact_data["consent_status"] == "MUTUAL_CONSENT_GRANTED"
    assert "+91" in contact_data["phone"]
