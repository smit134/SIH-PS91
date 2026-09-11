from .opportunity import router as opportunity_router
from .partner import router as partner_router
from .geospatial import router as geospatial_router

__all__ = ["opportunity_router", "partner_router", "geospatial_router"]
