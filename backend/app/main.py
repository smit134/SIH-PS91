"""ThinkForge Backend Main Application Entry Point.

Configures FastAPI, lifespan events, CORS middleware, global error handling,
and API routing.
"""

from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.config import settings
from app.core.exceptions import register_exception_handlers
from app.schemas.common import HealthResponse

# Intelligence / Independent Routers
from app.routers.opportunity import router as opportunity_router
from app.routers.partner import router as partner_router
from app.routers.geospatial import router as geospatial_router
from app.routers.finance import router as old_finance_router
from app.routers.schemes import router as schemes_router
from app.routers.users import router as users_router
from app.routers.chat import router as chat_router

# Configure structured logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("thinkforge.main")


from app.core.database import get_engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages application startup and shutdown lifecycle."""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} [{settings.ENVIRONMENT}]")
    
    # Ensure database tables exist
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


def create_application() -> FastAPI:
    """FastAPI Application Factory."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # CORS Middleware Configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Allow all for local dev integration
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register standardized exception handlers
    register_exception_handlers(app)

    # Mount API v1 router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Mount Independent Intelligence Routers
    app.include_router(opportunity_router)
    app.include_router(partner_router)
    app.include_router(geospatial_router)
    app.include_router(old_finance_router)
    app.include_router(schemes_router)
    app.include_router(users_router)
    app.include_router(chat_router, prefix="/api/chat", tags=["AI Chatbot"])

    @app.get(
        "/health",
        response_model=HealthResponse,
        status_code=status.HTTP_200_OK,
        tags=["System"],
        summary="Service Health Check",
    )
    async def health_check():
        """Returns service health status, application version, and timestamp."""
        return HealthResponse(
            status="ok",
            version=settings.VERSION,
            environment=settings.ENVIRONMENT,
        )

    @app.get(
        "/",
        status_code=status.HTTP_200_OK,
        tags=["System"],
        summary="Root Welcome Endpoint",
    )
    async def root():
        """Base welcome message and pointer to OpenAPI documentation."""
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "status": "online",
            "docs": "/docs",
            "features": [
                "Opportunity Fit Scoring (7-Factor)",
                "Reverse Business Search (Resource -> Business)",
                "Capability Gap Detection (6-Dimension)",
                "Partner Synergy & Matchmaking (Privacy-Preserving)",
                "Geospatial Proximity & Evidence Coverage"
            ]
        }

    return app


app = create_application()
