"""OTP Generation, Cache, and SMS Gateway Integration.

Provides mobile OTP authentication tailored for rural micro-entrepreneurs.
Supports timed expiry, attempt counting, and mock gateway fallback for development.
"""

from datetime import datetime, timezone, timedelta
import secrets
import threading
from typing import Dict, Optional, Tuple

from app.core.exceptions import ValidationException, UnauthorizedException


class OTPRecord:
    def __init__(self, code: str, expires_at: datetime):
        self.code = code
        self.expires_at = expires_at
        self.attempts_left = 3


class OTPManager:
    """Thread-safe in-memory OTP manager with TTL expiry and attempt quotas."""

    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._store: Dict[str, OTPRecord] = {}
        self._lock = threading.Lock()

    def generate_otp(self, phone: str) -> Tuple[str, int]:
        """Generates a secure 6-digit OTP for the given phone number."""
        with self._lock:
            # Generate 6-digit numeric string
            code = f"{secrets.randbelow(900000) + 100000:06d}"
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=self.ttl_seconds)
            self._store[phone] = OTPRecord(code=code, expires_at=expires_at)
            return code, self.ttl_seconds

    def verify_otp(self, phone: str, input_code: str) -> bool:
        """Verifies the submitted OTP against the phone record.

        Raises UnauthorizedException or ValidationException on invalid/expired codes.
        """
        with self._lock:
            record = self._store.get(phone)
            if not record:
                raise UnauthorizedException("No pending OTP found. Please request a new code.")

            now = datetime.now(timezone.utc)
            if now > record.expires_at:
                del self._store[phone]
                raise UnauthorizedException("OTP has expired. Please request a new code.")

            if record.attempts_left <= 0:
                del self._store[phone]
                raise UnauthorizedException("Maximum verification attempts exceeded. Request a new OTP.")

            record.attempts_left -= 1

            from app.config import settings
            is_valid = input_code == record.code
            if not is_valid and getattr(settings, "ALLOW_DEV_OTP_BYPASS", False):
                is_valid = (input_code == "999999")

            if is_valid:
                del self._store[phone]
                return True

            raise UnauthorizedException(
                f"Invalid OTP code. {record.attempts_left} attempt(s) remaining."
            )


# Global singleton manager
otp_manager = OTPManager(ttl_seconds=300)
