"""Rate Limiter Dependency for FastAPI Endpoints.

Provides sliding-window in-memory rate limiting to defend sensitive authentication
and SMS/OTP endpoints against brute-force credential stuffing and SMS flooding.
"""

from collections import defaultdict
from datetime import datetime, timezone
import threading
from typing import Dict, List
from fastapi import Request
from app.core.exceptions import APIException


class RateLimiter:
    """Sliding-window request rate limiter keyed by client identifier."""

    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._history: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def __call__(self, request: Request):
        # Extract client IP or forwarded IP
        client_ip = (
            request.headers.get("x-forwarded-for")
            or (request.client.host if request.client else "unknown")
        )
        now = datetime.now(timezone.utc).timestamp()
        window_start = now - self.window_seconds

        with self._lock:
            # Filter timestamps within current window
            timestamps = [ts for ts in self._history[client_ip] if ts > window_start]
            if len(timestamps) >= self.max_requests:
                raise APIException(
                    status_code=429,
                    code="RATE_LIMIT_EXCEEDED",
                    message=f"Too many requests. Maximum {self.max_requests} allowed per {self.window_seconds} seconds.",
                )

            timestamps.append(now)
            self._history[client_ip] = timestamps


# Preconfigured rate limiters for sensitive endpoints
auth_rate_limiter = RateLimiter(max_requests=10, window_seconds=60)
otp_send_rate_limiter = RateLimiter(max_requests=5, window_seconds=60)
