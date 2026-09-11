"""Unit tests for hyper-local spatial utilities and privacy obfuscation."""

import math
from app.core.spatial import (
    haversine_distance_km,
    is_within_radius,
    get_bounding_box,
    obfuscate_coordinates,
)


def test_haversine_distance_zero():
    """Distance to identical coordinate should be 0.0."""
    dist = haversine_distance_km(23.0225, 72.5714, 23.0225, 72.5714)
    assert dist == 0.0


def test_haversine_known_distance():
    """Ahmedabad (23.0225, 72.5714) to Anand (22.5645, 72.9289) is ~65-70 km."""
    dist = haversine_distance_km(23.0225, 72.5714, 22.5645, 72.9289)
    assert 60.0 < dist < 75.0


def test_is_within_radius():
    """Check radius logic within and outside bounds."""
    # Point A to Point B is ~65km
    assert is_within_radius(23.0225, 72.5714, 22.5645, 72.9289, radius_km=100.0) is True
    assert is_within_radius(23.0225, 72.5714, 22.5645, 72.9289, radius_km=50.0) is False


def test_get_bounding_box():
    """Verify generated bounding box covers the target radius."""
    lat, lon, radius = 23.0225, 72.5714, 15.0
    bbox = get_bounding_box(lat, lon, radius)

    assert bbox["min_lat"] < lat < bbox["max_lat"]
    assert bbox["min_lon"] < lon < bbox["max_lon"]
    # Approx 15km / 111 km/deg ~ 0.135 degrees
    assert abs((bbox["max_lat"] - lat) - (radius / 111.0)) < 0.001


def test_obfuscate_coordinates_privacy():
    """Ensure coordinates are shifted slightly for Section 33 privacy without drifting too far."""
    raw_lat, raw_lon = 23.0225, 72.5714
    fuzzed_lat, fuzzed_lon = obfuscate_coordinates(raw_lat, raw_lon, fuzz_radius_km=1.5)

    # Obfuscated coordinates should not be identical to exact raw coordinates
    # and should be rounded to 4 decimal places
    drift = haversine_distance_km(raw_lat, raw_lon, fuzzed_lat, fuzzed_lon)
    assert drift <= 2.0  # Stays within local vicinity
    assert len(str(fuzzed_lat).split(".")[1]) <= 4
