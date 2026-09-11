"""Integration tests for teammate handshake endpoints, OpenAPI contract conformity, and security."""

import uuid
import pytest
from app.seed.seed_data import seed_all
from app.models.evidence import EvidenceRecord


@pytest.fixture
async def auth_headers(client, test_db_session):
    """Creates a user with seeded database and returns auth headers."""
    await seed_all(test_db_session)
    phone_suffix = f"{uuid.uuid4().int % 100000000:08d}"
    payload = {
        "phone": f"+9199{phone_suffix}",
        "password": "passWord12345!",
        "full_name": "Integration Tester",
        "language": "en",
    }
    res = await client.post("/api/v1/auth/register", json=payload)
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
async def test_openapi_schema_contains_all_team_endpoints(client):
    """Verifies that FastAPI OpenAPI schema exposes all team member endpoints."""
    res = await client.get("/openapi.json")
    assert res.status_code == 200
    schema = res.json()
    paths = schema["paths"]

    # Core
    assert "/health" in paths
    assert "/api/v1/auth/register" in paths
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/profile" in paths

    # Aishwarya's contracts
    assert "/api/v1/businesses/recommendations" in paths
    assert "/api/v1/partners/recommendations" in paths

    # Kesha's contracts
    assert "/api/v1/finance/simulate" in paths
    assert "/api/v1/schemes/matches" in paths

    # Smit's contracts
    assert "/api/v1/evidence/nearby" in paths


@pytest.mark.anyio
async def test_business_recommendations_contract(client, auth_headers):
    """Verifies Aishwarya's business recommendation endpoint returns valid benchmark opportunities."""
    res = await client.get("/api/v1/businesses/recommendations?limit=3", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0

    first = data[0]
    assert "category_code" in first
    assert "category_name" in first
    assert "feasibility_score" in first
    assert 0.0 <= first["feasibility_score"] <= 100.0
    assert "risk_level" in first
    assert "break_even_months" in first
    assert "rationale" in first


@pytest.mark.anyio
async def test_partner_recommendations_contract(client, auth_headers):
    """Verifies Aishwarya's partner recommendation endpoint."""
    res = await client.get("/api/v1/partners/recommendations?radius_km=50", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)


@pytest.mark.anyio
async def test_finance_simulation_viable_scenario(client, auth_headers):
    """Verifies Kesha's financial simulation model in a profitable scenario."""
    payload = {
        "capital_invested": 100000.0,
        "monthly_revenue_projected": 45000.0,
        "monthly_expenses_projected": 25000.0,
    }
    res = await client.post("/api/v1/finance/simulate", json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["capital_invested"] == 100000.0
    assert data["monthly_net_profit"] == 20000.0
    assert data["profit_margin_pct"] == 44.44
    assert data["break_even_months"] == 5.0  # 100000 / 20000 = 5 months
    assert data["is_viable"] is True


@pytest.mark.anyio
async def test_finance_simulation_loss_scenario(client, auth_headers):
    """Verifies Kesha's financial simulation model in a loss/burn scenario."""
    payload = {
        "capital_invested": 60000.0,
        "monthly_revenue_projected": 10000.0,
        "monthly_expenses_projected": 20000.0,
    }
    res = await client.post("/api/v1/finance/simulate", json=payload, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["monthly_net_profit"] == -10000.0
    assert data["runway_months"] == 6.0  # 60000 / 10000 = 6 months
    assert data["is_viable"] is False


@pytest.mark.anyio
async def test_schemes_matches_contract(client, auth_headers):
    """Verifies Kesha's government scheme matching endpoint."""
    res = await client.get("/api/v1/schemes/matches", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0

    first = data[0]
    assert "scheme_name" in first
    assert "short_code" in first
    assert "max_loan_amount" in first
    assert "eligibility_verdict" in first


@pytest.mark.anyio
async def test_evidence_nearby_contract(client, auth_headers, test_db_session):
    """Verifies Smit's ground-truth field evidence endpoint with reliability classes."""
    # Seed a verified evidence record
    rec = EvidenceRecord(
        source_name="Amul Village Dairy Cooperative Collection Center",
        evidence_type="PRICE",
        reliability_class="VERIFIED",
        confidence_score=95,
        payload={"metric_name": "raw_milk_procurement_price_per_litre", "price_inr": 38.50},
        latitude=23.0225,
        longitude=72.5714,
    )
    test_db_session.add(rec)
    await test_db_session.commit()

    res = await client.get("/api/v1/evidence/nearby?reliability=VERIFIED", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
    assert any(d["reliability_class"] == "VERIFIED" for d in data)
    assert any(d["source_name"] == "Amul Village Dairy Cooperative Collection Center" for d in data)




@pytest.mark.anyio
async def test_unauthenticated_requests_are_rejected(client):
    """Verifies that all integration endpoints reject unauthenticated calls with 401 Unauthorized."""
    endpoints = [
        ("GET", "/api/v1/businesses/recommendations"),
        ("GET", "/api/v1/partners/recommendations"),
        ("POST", "/api/v1/finance/simulate"),
        ("GET", "/api/v1/schemes/matches"),
        ("GET", "/api/v1/evidence/nearby"),
    ]

    for method, path in endpoints:
        if method == "GET":
            res = await client.get(path)
        else:
            res = await client.post(path, json={})
        assert res.status_code == 401, f"Expected 401 for unauthenticated {method} {path}"
