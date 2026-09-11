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
