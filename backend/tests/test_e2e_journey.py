"""End-to-End Verification of Complete Entrepreneur Journey and Integration Handshake.

Executes a live simulated lifecycle test through all 14 steps of Dhruv's backend scope.
"""

import uuid
import pytest
from app.seed.seed_data import seed_all
from app.models.evidence import EvidenceRecord


@pytest.mark.anyio
async def test_full_entrepreneur_e2e_lifecycle(client, test_db_session):
    """Executes the complete entrepreneur lifecycle from onboarding to financial simulation."""
    # 0. Seed benchmark data
    await seed_all(test_db_session)

    # 1. Register User
    phone = f"+9198{uuid.uuid4().int % 100000000:08d}"
    reg_payload = {
        "phone": phone,
        "password": "Password123!",
        "full_name": "Savitri Patel",
        "language": "gu",
    }
    reg_res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    auth_data = reg_res.json()
    token = auth_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Login with Credentials
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"phone": phone, "password": "Password123!"},
    )
    assert login_res.status_code == 200

    # 3. Request and Verify Mobile OTP
    otp_send_res = await client.post("/api/v1/auth/otp/send", json={"phone": phone})
    assert otp_send_res.status_code == 200
    assert otp_send_res.json()["is_registered_user"] is True

    otp_verify_res = await client.post(
        "/api/v1/auth/otp/verify",
        json={"phone": phone, "otp_code": "999999"},
    )
    assert otp_verify_res.status_code == 200

    # 4. Fetch /auth/me
    me_res = await client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["user"]["phone"] == phone

    # 5. Update Profile with Capital and Location
    update_payload = {
        "full_name": "Savitri Patel",
        "available_capital": 65000,
        "latitude": 23.0225,
        "longitude": 72.5714,
        "approx_location_name": "Ahmedabad Rural",
        "risk_tolerance": "LOW",
        "experience_years": 3,
    }
    profile_res = await client.put("/api/v1/profile", json=update_payload, headers=headers)
    assert profile_res.status_code == 200
    assert profile_res.json()["available_capital"] == 65000

    # 6. Add Capability Skill
    skill_payload = {
        "name": "Organic Food Preservation",
        "proficiency": "EXPERT",
        "category": "PRODUCTION",
    }
    skill_res = await client.post("/api/v1/profile/skills", json=skill_payload, headers=headers)
    assert skill_res.status_code == 201

    # 7. Add Physical Asset / Machinery Resource
    resource_payload = {
        "name": "Cold Storage Unit 500L",
        "resource_type": "STORAGE",
        "details": "500 Litres capacity solar powered",
    }
    res_res = await client.post("/api/v1/profile/resources", json=resource_payload, headers=headers)
    assert res_res.status_code == 201


    # 8. Check Profile Readiness Score
    readiness_res = await client.get("/api/v1/profile/readiness", headers=headers)
    assert readiness_res.status_code == 200
    readiness_data = readiness_res.json()
    assert readiness_data["readiness_percentage"] >= 75
    assert len(readiness_data["completed_sections"]) >= 3
    assert isinstance(readiness_data["recommendations"], list)



    # 9. Get AI Business Opportunity Recommendations (Aishwarya Handshake)
    rec_res = await client.get("/api/v1/businesses/recommendations?limit=3", headers=headers)
    assert rec_res.status_code == 200
    recommendations = rec_res.json()
    assert len(recommendations) >= 3
    assert any(r["feasibility_score"] >= 80 for r in recommendations)

    # 10. Discover Local Partners within 50km (Aishwarya Handshake)
    partner_res = await client.get("/api/v1/partners/recommendations?radius_km=50", headers=headers)
    assert partner_res.status_code == 200

    # 11. Run Financial Feasibility Simulation (Kesha Handshake)
    sim_payload = {
        "capital_invested": 65000.0,
        "monthly_revenue_projected": 30000.0,
        "monthly_expenses_projected": 18000.0,
    }
    sim_res = await client.post("/api/v1/finance/simulate", json=sim_payload, headers=headers)
    assert sim_res.status_code == 200
    sim_data = sim_res.json()
    assert sim_data["is_viable"] is True
    assert sim_data["monthly_net_profit"] == 12000.0
    assert sim_data["break_even_months"] == 5.4  # 65000 / 12000 ~ 5.4

    # 12. Match Government Credit Schemes (Kesha Handshake)
    scheme_res = await client.get("/api/v1/schemes/matches", headers=headers)
    assert scheme_res.status_code == 200
    schemes = scheme_res.json()
    assert len(schemes) >= 3
    assert any(s["short_code"] == "MUDRA" for s in schemes)

    # 13. Query Nearby Field Evidence with Section 33 Reliability Class (Smit Handshake)
    evidence = EvidenceRecord(
        source_name="e-NAM Agmarknet Mandi Feed",
        evidence_type="PRICE",
        reliability_class="VERIFIED",
        confidence_score=98,
        payload={"commodity": "Mustard Oil", "mandi_modal_price_per_quintal": 5400},
        latitude=23.0225,
        longitude=72.5714,
    )
    test_db_session.add(evidence)
    await test_db_session.commit()

    ev_res = await client.get("/api/v1/evidence/nearby?reliability=VERIFIED", headers=headers)
    assert ev_res.status_code == 200
    ev_list = ev_res.json()
    assert len(ev_list) >= 1
    assert ev_list[0]["reliability_class"] == "VERIFIED"
    assert ev_list[0]["source_name"] == "e-NAM Agmarknet Mandi Feed"
