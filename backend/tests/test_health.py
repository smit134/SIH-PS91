"""Tests for Health and Root Endpoints."""

import pytest


@pytest.mark.anyio
async def test_health_check_endpoint(client):
    """Verifies GET /health returns 200 and expected schema."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data


@pytest.mark.anyio
async def test_root_endpoint(client):
    """Verifies GET / returns 200 and docs pointer."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["docs"] == "/docs"
