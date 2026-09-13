"""
API Endpoint tests using FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["docs"] == "/docs"


def test_catalog_endpoint():
    response = client.get("/api/intelligence/opportunity/catalog")
    assert response.status_code == 200
    catalog = response.json()
    assert len(catalog) >= 5
    assert any(b["id"] == "handicraft_textiles" for b in catalog)


def test_reverse_search_endpoint():
    payload = {
        "user_id": "test_api_user",
        "name": "Sunil Kumar",
        "available_capital": 25000.0,
        "skills": ["Composting", "Organic Farming"],
        "experience_years": 2.0,
        "resources": ["Shaded Land", "Water Source"],
        "interests": ["vermicompost_production"],
        "location": {
            "latitude": 28.5900,
            "longitude": 77.1950,
            "service_radius_km": 10.0
        },
        "risk_preference": "Low",
        "has_market_connections": False,
        "has_transport_access": False,
        "has_digital_tools": False
    }

    response = client.post("/api/intelligence/opportunity/reverse-search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_evaluated"] >= 5
    assert data["top_recommended"]["business_id"] == "vermicompost_production"


def test_partner_recommendations_endpoint():
    payload = {
        "user_id": "artisan_api",
        "name": "Artisan",
        "available_capital": 30000.0,
        "skills": ["Handicraft"],
        "experience_years": 3.0,
        "resources": ["Workspace"],
        "interests": ["handicraft_textiles"],
        "location": {
            "latitude": 28.6140,
            "longitude": 77.2090,
            "service_radius_km": 10.0
        },
        "risk_preference": "Medium",
        "has_market_connections": False,
        "has_transport_access": False,
        "has_digital_tools": False
    }

    response = client.post("/api/intelligence/partner/recommendations", json=payload)
    assert response.status_code == 200
    cards = response.json()
    assert len(cards) >= 1
    assert cards[0]["synergy_score"] > 70.0


def test_local_evidence_snapshot_endpoint():
    response = client.get("/api/intelligence/geospatial/evidence-snapshot?latitude=28.6140&longitude=77.2090&radius_km=10.0")
    assert response.status_code == 200
    data = response.json()
    assert "local_opportunity_composite" in data
    assert "overall_evidence_coverage_percentage" in data
    assert len(data["coverage_breakdown"]) >= 4
