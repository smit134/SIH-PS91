"""Hyper-Local Geospatial Calculations and Privacy Obfuscation.

Provides Haversine distance computations, radius checks, bounding boxes,
and coordinate fuzzing for Section 33 privacy compliance.
"""

import math
from typing import Dict, Tuple

EARTH_RADIUS_KM = 6371.0


def haversine_distance_km(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """Calculates the great-circle distance between two geographic points in kilometers."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(EARTH_RADIUS_KM * c, 3)


def is_within_radius(
    center_lat: float,
    center_lon: float,
    target_lat: float,
    target_lon: float,
    radius_km: float,
) -> bool:
    """Checks whether a target coordinate falls within a specified radius from center."""
    distance = haversine_distance_km(center_lat, center_lon, target_lat, target_lon)
    return distance <= radius_km


def get_bounding_box(
    lat: float, lon: float, radius_km: float
) -> Dict[str, float]:
    """Generates bounding box coordinates for rapid SQL pre-filtering."""
    lat_delta = radius_km / 111.0
    lon_delta = radius_km / (111.0 * math.cos(math.radians(lat)))

    return {
        "min_lat": round(lat - lat_delta, 6),
        "max_lat": round(lat + lat_delta, 6),
        "min_lon": round(lon - lon_delta, 6),
        "max_lon": round(lon + lon_delta, 6),
    }


def obfuscate_coordinates(
    lat: float, lon: float, fuzz_radius_km: float = 1.0
) -> Tuple[float, float]:
    """Fuzzes exact coordinates to village/district vicinity for Section 33 privacy.

    Ensures rural entrepreneurs' exact domestic addresses are never publicly exposed.
    """
    # Deterministic displacement based on coordinate hashes to preserve stable display
    hash_seed = int((lat + 90.0) * 1000 + (lon + 180.0) * 1000)
    angle = (hash_seed % 360) * (math.pi / 180.0)
    offset_km = ((hash_seed % 80) / 100.0) * fuzz_radius_km  # between 0 and 0.8 * fuzz

    lat_offset = (offset_km / 111.0) * math.sin(angle)
    lon_offset = (offset_km / (111.0 * math.cos(math.radians(lat)))) * math.cos(angle)

    return (round(lat + lat_offset, 4), round(lon + lon_offset, 4))
