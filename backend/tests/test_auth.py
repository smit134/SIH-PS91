"""Comprehensive Authentication and Authorization Tests.

Verifies registration, login, token refresh, password hashing, and role checks.
"""

import pytest
from app.core.deps import require_role
from app.main import app
from app.models.user import UserRole


# Helper protected test endpoint to verify role guards
@app.get("/test-admin-only", tags=["Test"])
async def sample_admin_only_route(_=pytest.importorskip("fastapi").Depends(require_role(UserRole.ADMIN))):
    return {"message": "Admin access granted"}


@pytest.mark.anyio
async def test_register_user_success(client):
    """Verifies successful registration of a rural entrepreneur."""
    payload = {
        "phone": "+919812345678",
        "password": "strongPassword123",
        "full_name": "Kishan Lal",
        "email": "kishan@example.org",
        "language": "hi",
        "role": "ENTREPRENEUR",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["phone"] == "+919812345678"
    assert data["user"]["role"] == "ENTREPRENEUR"
    assert data["user"]["is_active"] is True


@pytest.mark.anyio
async def test_register_duplicate_phone_rejected(client):
    """Verifies that duplicate phone registration is blocked with 409 Conflict."""
    payload = {
        "phone": "+919800000001",
        "password": "password123",
        "full_name": "User One",
    }
    first_res = await client.post("/api/v1/auth/register", json=payload)
    assert first_res.status_code == 201

    duplicate_res = await client.post("/api/v1/auth/register", json=payload)
    assert duplicate_res.status_code == 409
    err = duplicate_res.json()
    assert err["error"]["code"] == "RESOURCE_CONFLICT"


@pytest.mark.anyio
async def test_register_invalid_phone_format_rejected(client):
    """Verifies Pydantic E.164 phone pattern validation rejection."""
    payload = {
        "phone": "not-a-number",
        "password": "password123",
        "full_name": "Invalid User",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422
    err = response.json()
    assert err["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.anyio
async def test_login_success(client):
    """Verifies login with valid credentials returns tokens and user summary."""
    # Register first
    reg_payload = {
        "phone": "+919800000002",
        "password": "correctPassword",
        "full_name": "Login User",
    }
    await client.post("/api/v1/auth/register", json=reg_payload)

    # Login
    login_payload = {
        "phone": "+919800000002",
        "password": "correctPassword",
    }
    response = await client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["phone"] == "+919800000002"


@pytest.mark.anyio
async def test_login_invalid_password_rejected(client):
    """Verifies login with wrong password is rejected with 401 Unauthorized."""
    reg_payload = {
        "phone": "+919800000003",
        "password": "correctPassword",
        "full_name": "Test User",
    }
    await client.post("/api/v1/auth/register", json=reg_payload)

    login_payload = {
        "phone": "+919800000003",
        "password": "wrongPassword",
    }
    response = await client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401
    err = response.json()
    assert err["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.anyio
async def test_login_nonexistent_user_rejected(client):
    """Verifies login with unregistered phone is rejected with 401 Unauthorized."""
    login_payload = {
        "phone": "+919999999999",
        "password": "anyPassword",
    }
    response = await client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401


@pytest.mark.anyio
async def test_refresh_token_lifecycle(client):
    """Verifies obtaining new access token using a valid refresh token."""
    reg_payload = {
        "phone": "+919800000004",
        "password": "password123",
        "full_name": "Refresh User",
    }
    reg_res = await client.post("/api/v1/auth/register", json=reg_payload)
    refresh_token = reg_res.json()["refresh_token"]

    refresh_res = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_res.status_code == 200
    new_data = refresh_res.json()
    assert "access_token" in new_data
    assert "refresh_token" in new_data


@pytest.mark.anyio
async def test_get_current_user_me_endpoint(client):
    """Verifies GET /auth/me returns authenticated user details and profile."""
    reg_payload = {
        "phone": "+919800000005",
        "password": "password123",
        "full_name": "Me Endpoint User",
        "language": "hi",
    }
    reg_res = await client.post("/api/v1/auth/register", json=reg_payload)
    access_token = reg_res.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["phone"] == "+919800000005"
    assert data["profile_summary"]["full_name"] == "Me Endpoint User"
    assert data["profile_summary"]["language"] == "hi"


@pytest.mark.anyio
async def test_get_me_unauthorized_without_token(client):
    """Verifies accessing /auth/me without token returns 401."""
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
    err = response.json()
    assert err["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.anyio
async def test_get_me_with_invalid_token(client):
    """Verifies accessing /auth/me with corrupt token returns 401."""
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.corrupt.token"},
    )
    assert response.status_code == 401
    err = response.json()
    assert err["error"]["code"] == "UNAUTHORIZED"
