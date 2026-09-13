"""OpenStreetMap Point-of-Interest Model (PostGIS-backed).

Stores real POIs imported from Geofabrik OSM extracts for Gujarat.
Used by the Geospatial Engine for ST_DWithin proximity queries.
"""

from typing import Optional
from geoalchemy2 import Geometry
from sqlalchemy import BigInteger, Float, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class OSMPointOfInterest(Base):
    """Real-world Point of Interest imported from OpenStreetMap."""

    __tablename__ = "osm_pois"

    osm_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=False,
        comment="Original OpenStreetMap node ID",
    )
    name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="POI name from OSM tags",
    )
    poi_category: Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False,
        comment="Normalized category: market, bank, transport, school, hospital, cold_storage, etc.",
    )
    amenity: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Raw OSM amenity tag value",
    )
    shop: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Raw OSM shop tag value",
    )
    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="WGS84 latitude",
    )
    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="WGS84 longitude",
    )
    geom: Mapped[Optional[str]] = mapped_column(
        Geometry("POINT", srid=4326),
        nullable=True,
        comment="PostGIS POINT geometry for spatial queries",
    )
    state: Mapped[str] = mapped_column(
        String(50),
        default="Gujarat",
        nullable=False,
        comment="Indian state",
    )
    district: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="District name if available",
    )
    raw_tags: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="JSON string of all original OSM tags for this node",
    )

    __table_args__ = (
        Index("idx_osm_pois_category_state", "poi_category", "state"),
    )
