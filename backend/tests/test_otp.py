"""Unit and integration tests for SMS OTP authentication and rate limiting."""

from datetime import datetime, timezone, timedelta
import uuid
import pytest

from app.core.otp import otp_manager, OTPRecord


@pytest.mark.anyio
async def test_send_otp_success(client):
    """Verifies that requesting an OTP returns a dispatch confirmation with TTL."""
    phone = f"+9198{uuid.uuid4().int % 100000000:08d}"
    payload = {"phone": phone}

    res = await client.post("/api/v1/auth/otp/send", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["phone"] == phone
    assert data["expires_in_seconds"] == 300
    assert data["is_registered_user"] is False


@pytest.mark.anyio
async def test_verify_otp_new_user_auto_onboard(client):
    """Verifies that submitting a valid OTP for an unregistered number automatically onboards the user."""
    phone = f"+9198{uuid.uuid4().int % 100000000:08d}"

    # Step 1: Send OTP
    send_res = await client.post("/api/v1/auth/otp/send", json={"phone": phone})
    assert send_res.status_code == 200

    # Step 2: Verify using development bypass or valid OTP
    verify_payload = {
        "phone": phone,
        "otp_code": "999999",
        "full_name": "Savitri Devi",
        "language": "hi",
    }
    verify_res = await client.post("/api/v1/auth/otp/verify", json=verify_payload)
    assert verify_res.status_code == 200
    data = verify_res.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["phone"] == phone
    assert data["user"]["is_verified"] is True


@pytest.mark.anyio
async def test_verify_otp_existing_user_login(client):
    """Verifies that submitting valid OTP for an existing user authenticates without altering profile."""
    phone = f"+9198{uuid.uuid4().int % 100000000:08d}"

    # First register user with password
    reg_payload = {
        "phone": phone,
        "password": "strongPassword123",
        "full_name": "Kavita Bai",
    }
    reg_res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201

    # Request OTP
    send_res = await client.post("/api/v1/auth/otp/send", json={"phone": phone})
    assert send_res.status_code == 200
    assert send_res.json()["is_registered_user"] is True

    # Verify OTP
    verify_res = await client.post(
        "/api/v1/auth/otp/verify",
        json={"phone": phone, "otp_code": "999999"},
    )
    assert verify_res.status_code == 200
    data = verify_res.json()
    assert data["user"]["phone"] == phone


@pytest.mark.anyio
async def test_verify_otp_invalid_code_rejected(client):
    """Verifies that an incorrect OTP code is rejected with 401 Unauthorized."""
    phone = f"+9198{uuid.uuid4().int % 100000000:08d}"
    await client.post("/api/v1/auth/otp/send", json={"phone": phone})

    verify_res = await client.post(
        "/api/v1/auth/otp/verify",
        json={"phone": phone, "otp_code": "000000"},
    )
    assert verify_res.status_code == 401
    assert "Invalid OTP code" in verify_res.json()["error"]["message"]


@pytest.mark.anyio
async def test_verify_otp_expired_code_rejected(client):
    """Verifies that an expired OTP code is rejected."""
    phone = f"+9198{uuid.uuid4().int % 100000000:08d}"

    # Manually store expired OTP record
    past_time = datetime.now(timezone.utc) - timedelta(seconds=10)
    otp_manager._store[phone] = OTPRecord(code="123456", expires_at=past_time)

    verify_res = await client.post(
        "/api/v1/auth/otp/verify",
        json={"phone": phone, "otp_code": "123456"},
    )
    assert verify_res.status_code == 401
    assert "expired" in verify_res.json()["error"]["message"].lower()



@pytest.mark.anyio
async def test_rate_limiter_exceeded(client):
    """Verifies that rapid requests trigger HTTP 429 Too Many Requests."""
    from app.core.rate_limiter import RateLimiter
    from fastapi import Request
    from app.core.exceptions import APIException

    limiter = RateLimiter(max_requests=3, window_seconds=60)

    class DummyClient:
        host = "192.168.1.100"

    class DummyRequest:
        headers = {}
        client = DummyClient()

    req = DummyRequest()

    # First 3 should succeed
    limiter(req)
    limiter(req)
    limiter(req)

    # 4th request must raise APIException with status 429
    with pytest.raises(APIException) as exc_info:
        limiter(req)

    assert exc_info.value.status_code == 429
    assert exc_info.value.code == "RATE_LIMIT_EXCEEDED"

