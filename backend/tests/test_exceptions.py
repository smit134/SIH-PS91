"""Tests for Standardized Error Envelopes and Exception Handlers."""

import pytest
from pydantic import BaseModel, Field
from app.core.exceptions import NotFoundException, ConflictException, UnauthorizedException
from app.main import app


# Temporary test route model for validation testing
class SampleInput(BaseModel):
    phone: str = Field(..., min_length=10)
    capital: int = Field(..., gt=0)


@app.post("/test-validation", tags=["Test"])
async def sample_validation_route(payload: SampleInput):
    return {"success": True}


@app.get("/test-custom-exception", tags=["Test"])
async def sample_custom_exception():
    raise ConflictException(message="Sample conflict message")


@pytest.mark.anyio
async def test_404_error_envelope(client):
    """Verifies unmapped route returns standardized error envelope."""
    response = await client.get("/non-existent-route")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "RESOURCE_NOT_FOUND"
    assert "message" in data["error"]
    assert "timestamp" in data["error"]


@pytest.mark.anyio
async def test_422_validation_error_envelope(client):
    """Verifies validation failure returns standardized error envelope with field details."""
    response = await client.post("/test-validation", json={"phone": "123", "capital": -5})
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert isinstance(data["error"]["details"], list)
    assert len(data["error"]["details"]) > 0


@pytest.mark.anyio
async def test_custom_conflict_exception(client):
    """Verifies custom APIException produces proper status and error code."""
    response = await client.get("/test-custom-exception")
    assert response.status_code == 409
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "RESOURCE_CONFLICT"
    assert data["error"]["message"] == "Sample conflict message"
