"""V1 API Router Aggregator.

Central entry point mounting all modular domain routers.
"""

from fastapi import APIRouter

from app.api.v1 import auth, profile, businesses, partners, finance, evidence

api_router = APIRouter()

# Core Authentication & Profile routers (Dhruv)
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])

# Integration & Handshake Router Stubs for Team Members
api_router.include_router(businesses.router)
api_router.include_router(partners.router)
api_router.include_router(finance.router)
api_router.include_router(evidence.router)

