"""Tests for Entrepreneur Profile Management and Readiness Calculator."""

import pytest


import uuid


@pytest.fixture
async def auth_headers(client):
    """Registers a fresh user and returns Bearer auth headers."""
    phone_suffix = f"{uuid.uuid4().int % 100000000:08d}"
    payload = {
        "phone": f"+9198{phone_suffix}",
        "password": "strongPassword123",
        "full_name": "Radha Sharma",
        "language": "hi",
    }
    res = await client.post("/api/v1/auth/register", json=payload)
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
async def test_get_profile_initial_state(client, auth_headers):
    """Verifies fetching initial capability profile."""
    response = await client.get("/api/v1/profile", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Radha Sharma"
    assert data["language"] == "hi"
    assert data["available_capital"] == 0
    assert data["skills"] == []
    assert data["resources"] == []


@pytest.mark.anyio
async def test_update_profile(client, auth_headers):
    """Verifies updating profile attributes and geographic coordinates."""
    update_payload = {
        "full_name": "Radha Sharma Ji",
        "available_capital": 85000,
        "latitude": 23.0225,
        "longitude": 72.5714,
        "approx_location_name": "Anand, Gujarat",
        "risk_tolerance": "LOW",
        "experience_years": 4,
    }
    response = await client.put(
        "/api/v1/profile",
        json=update_payload,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Radha Sharma Ji"
    assert data["available_capital"] == 85000
    assert data["latitude"] == 23.0225
    assert data["risk_tolerance"] == "LOW"
    assert data["experience_years"] == 4


@pytest.mark.anyio
async def test_add_and_remove_skill(client, auth_headers):
    """Verifies adding a skill and subsequently removing it."""
    skill_payload = {
        "name": "Terracotta Pottery",
        "category": "CRAFT",
        "proficiency": "EXPERT",
    }
    add_res = await client.post(
        "/api/v1/profile/skills",
        json=skill_payload,
        headers=auth_headers,
    )
    assert add_res.status_code == 201
    skill_data = add_res.json()
    assert skill_data["name"] == "Terracotta Pottery"
    assert skill_data["proficiency"] == "EXPERT"
    skill_id = skill_data["skill_id"]

    # Verify skill appears in profile
    prof_res = await client.get("/api/v1/profile", headers=auth_headers)
    assert len(prof_res.json()["skills"]) == 1

    # Remove skill
    del_res = await client.delete(
        f"/api/v1/profile/skills/{skill_id}",
        headers=auth_headers,
    )
    assert del_res.status_code == 200

    # Verify skill is removed
    prof_res_after = await client.get("/api/v1/profile", headers=auth_headers)
    assert len(prof_res_after.json()["skills"]) == 0


@pytest.mark.anyio
async def test_add_and_remove_resource(client, auth_headers):
    """Verifies adding a physical asset and subsequently removing it."""
    resource_payload = {
        "name": "Electric Kiln & Pottery Wheel",
        "resource_type": "EQUIPMENT",
        "details": "220V 5kW pottery kiln",
    }
    add_res = await client.post(
        "/api/v1/profile/resources",
        json=resource_payload,
        headers=auth_headers,
    )
    assert add_res.status_code == 201
    res_data = add_res.json()
    assert res_data["name"] == "Electric Kiln & Pottery Wheel"
    assert res_data["resource_type"] == "EQUIPMENT"
    resource_id = res_data["resource_id"]

    # Verify resource appears in profile
    prof_res = await client.get("/api/v1/profile", headers=auth_headers)
    assert len(prof_res.json()["resources"]) == 1

    # Remove resource
    del_res = await client.delete(
        f"/api/v1/profile/resources/{resource_id}",
        headers=auth_headers,
    )
    assert del_res.status_code == 200

    # Verify resource is removed
    prof_res_after = await client.get("/api/v1/profile", headers=auth_headers)
    assert len(prof_res_after.json()["resources"]) == 0


@pytest.mark.anyio
async def test_profile_readiness_calculator(client, auth_headers):
    """Verifies readiness percentage increases as profile sections are populated."""
    # 1. Initial state (only identity filled = 20%)
    initial_res = await client.get("/api/v1/profile/readiness", headers=auth_headers)
    assert initial_res.status_code == 200
    initial_data = initial_res.json()
    assert initial_data["readiness_percentage"] == 20
    assert "Personal Identity" in initial_data["completed_sections"]
    assert "Geographic Location" in initial_data["missing_sections"]

    # 2. Add location and capital (+40% -> 60%)
    await client.put(
        "/api/v1/profile",
        json={"latitude": 23.0, "longitude": 72.5, "available_capital": 50000},
        headers=auth_headers,
    )

    # 3. Add skill (+20% -> 80%)
    await client.post(
        "/api/v1/profile/skills",
        json={"name": "Embroidery", "category": "CRAFT", "proficiency": "EXPERT"},
        headers=auth_headers,
    )

    # 4. Add resource (+20% -> 100%)
    await client.post(
        "/api/v1/profile/resources",
        json={"name": "Sewing Machine", "resource_type": "EQUIPMENT"},
        headers=auth_headers,
    )

    full_res = await client.get("/api/v1/profile/readiness", headers=auth_headers)
    assert full_res.status_code == 200
    full_data = full_res.json()
    assert full_data["readiness_percentage"] == 100
    assert len(full_data["missing_sections"]) == 0
    assert len(full_data["completed_sections"]) == 5
