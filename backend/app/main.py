"""
ThinkForge — SIH26091 Backend Application.
Intelligence Layer (Part 4 - Aishwarya): Opportunity & Partner Engines, Geospatial Intelligence.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.opportunity import router as opportunity_router
from .routers.partner import router as partner_router
from .routers.geospatial import router as geospatial_router

app = FastAPI(
    title="ThinkForge Intelligence Engines API",
    description="""
    AI-Driven Rural Business Advisory & Partner Intelligence Platform (SIH26091).
    Part 4 (Aishwarya) Modules:
    - 7-Factor Opportunity Fit Scoring & Explainability Engine
    - Reverse Business Search ('Resource -> Business')
    - 6D Capability Dashboard & Gap Analysis
    - Complementary Partner Matching & Synergy Scoring (Privacy-Preserving)
    - Geospatial Proximity & Hyper-Local Evidence Layer
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for Frontend integration (Madhav / Harshanshu)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Intelligence Routers
app.include_router(opportunity_router)
app.include_router(partner_router)
app.include_router(geospatial_router)


@app.get("/", summary="Root Health Check")
async def root():
    return {
        "status": "healthy",
        "service": "ThinkForge Intelligence Engine",
        "assigned_to": "Aishwarya (Part 4)",
        "features": [
            "Opportunity Fit Scoring (7-Factor)",
            "Reverse Business Search (Resource -> Business)",
            "Capability Gap Detection (6-Dimension)",
            "Partner Synergy & Matchmaking (Privacy-Preserving)",
            "Geospatial Proximity & Evidence Coverage"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
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

# Configure structured logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("thinkforge.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages application startup and shutdown lifecycle."""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} [{settings.ENVIRONMENT}]")
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
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register standardized exception handlers
    register_exception_handlers(app)

    # Mount API v1 router
    app.include_router(api_router, prefix=settings.API_V1_STR)

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
        }

    return app


app = create_application()
