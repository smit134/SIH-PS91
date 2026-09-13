"""Geospatial Models for PostGIS mapping."""

from typing import Optional
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geometry

from app.core.database import Base


class BusinessPOI(Base):
    """Overture Maps Points of Interest / Business dataset."""
    __tablename__ = "business_poi"

    poi_id: Mapped[str] = mapped_column(String, index=True, nullable=False, comment="Overture ID or Hash")
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True, comment="Business Name")
    category: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True, comment="Main Category")
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="Overture Confidence Score")
    
    # Store exact coords for quick non-spatial queries if needed
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Geometry column created by geopandas is named "geometry"
    geometry = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=False
    )


class PopulationGrid(Base):
    """Kontur Population Density Hexagons."""
    __tablename__ = "population_grid"

    population: Mapped[int] = mapped_column(Integer, nullable=False, comment="Estimated population in this hexagon")
    
    # Geometry column created by geopandas is named "geometry"
    geometry = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=True),
        nullable=False
    )
