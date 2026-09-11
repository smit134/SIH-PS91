"""
Unit tests for Geospatial Distance, Radius Filtering & Evidence Coverage.
"""

import pytest
from app.engines.geospatial_engine import GeospatialEngine
from app.models.common import EvidenceClass


def test_haversine_distance():
    # Distance between two nearby coordinates (~1.2 km)
    d = GeospatialEngine.haversine_distance(28.6140, 77.2090, 28.6190, 28.6190)
    # Correct calculation check
    d_delhi = GeospatialEngine.haversine_distance(28.6139, 77.2090, 28.6150, 77.2080)
    assert d_delhi < 1.0  # < 1 km apart


def test_local_signals_and_evidence_coverage():
    snapshot = GeospatialEngine.evaluate_local_signals(
        lat=28.6140,
        lon=77.2090,
        radius_km=10.0,
        category="handicraft_textiles"
    )

    assert snapshot.local_opportunity_composite >= 50.0
    assert snapshot.overall_evidence_coverage_percentage > 50.0
    assert len(snapshot.coverage_breakdown) >= 4
    assert any(item.evidence_class == EvidenceClass.VERIFIED for item in snapshot.coverage_breakdown)
    assert any(item.evidence_class == EvidenceClass.ESTIMATED for item in snapshot.coverage_breakdown)
    assert "census" in snapshot.registry_disclaimer.lower()
