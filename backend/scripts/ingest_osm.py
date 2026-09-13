"""Ingest OpenStreetMap POIs from .osm.pbf into PostGIS osm_pois table.

Usage:
    python -m scripts.ingest_osm [--pbf-file data/raw/osm/gujarat-latest.osm.pbf] [--dry-run]

Download Gujarat OSM data:
    curl -O https://download.geofabrik.de/asia/india/gujarat-latest.osm.pbf
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_sessionmaker, get_engine, Base
from app.models.osm_poi import OSMPointOfInterest

# --- OSM Tag → ThinkForge POI Category Mapping ---
AMENITY_CATEGORY_MAP = {
    # Markets & Commerce
    "marketplace": "market",
    "market": "market",
    # Banks
    "bank": "bank",
    "atm": "bank",
    # Transport
    "bus_station": "transport",
    "taxi": "transport",
    "ferry_terminal": "transport",
    "fuel": "transport",
    # Education
    "school": "school",
    "college": "school",
    "university": "school",
    "library": "school",
    # Healthcare
    "hospital": "hospital",
    "clinic": "hospital",
    "doctors": "hospital",
    "pharmacy": "hospital",
    "veterinary": "hospital",
    # Cold Storage / Warehousing
    "cold_storage": "cold_storage",
    "warehouse": "cold_storage",
    # Government
    "post_office": "government",
    "townhall": "government",
    "community_centre": "government",
    "police": "government",
    "courthouse": "government",
}

SHOP_CATEGORY_MAP = {
    "supermarket": "market",
    "wholesale": "market",
    "general": "market",
    "convenience": "market",
    "greengrocer": "market",
    "farm": "market",
    "hardware": "market",
    "clothes": "market",
    "electronics": "market",
}

RAILWAY_CATEGORIES = {"station", "halt", "stop"}


def classify_osm_node(tags: dict) -> str | None:
    """Classify an OSM node into a ThinkForge POI category. Returns None if irrelevant."""
    amenity = tags.get("amenity", "")
    shop = tags.get("shop", "")
    railway = tags.get("railway", "")
    landuse = tags.get("landuse", "")
    building = tags.get("building", "")
    
    if amenity in AMENITY_CATEGORY_MAP:
        return AMENITY_CATEGORY_MAP[amenity]
    
    if shop in SHOP_CATEGORY_MAP:
        return SHOP_CATEGORY_MAP[shop]
    
    if shop:  # Any shop is a market
        return "market"
    
    if railway in RAILWAY_CATEGORIES:
        return "transport"
    
    if landuse in ("industrial", "commercial"):
        return "industrial"
    
    if building == "warehouse":
        return "cold_storage"
    
    return None


def parse_osm_pbf(pbf_path: str) -> list:
    """Parse .osm.pbf file and extract relevant POIs."""
    try:
        import osmium
    except ImportError:
        print("ERROR: 'osmium' package not installed.")
        print("Install it: pip install osmium")
        sys.exit(1)
    
    print(f"  Parsing PBF file: {pbf_path}")
    
    class POIHandler(osmium.SimpleHandler):
        def __init__(self):
            super().__init__()
            self.pois = []
            self.count = 0
        
        def node(self, n):
            self.count += 1
            if self.count % 1000000 == 0:
                print(f"    Processed {self.count:,} nodes, found {len(self.pois)} POIs...")
            
            tags = dict(n.tags)
            category = classify_osm_node(tags)
            
            if category and n.location.valid():
                self.pois.append({
                    "osm_id": n.id,
                    "name": tags.get("name", tags.get("name:en", None)),
                    "poi_category": category,
                    "amenity": tags.get("amenity"),
                    "shop": tags.get("shop"),
                    "latitude": n.location.lat,
                    "longitude": n.location.lon,
                    "state": "Gujarat",
                    "district": tags.get("addr:district", tags.get("is_in:district", None)),
                    "raw_tags": json.dumps(tags) if len(tags) <= 20 else None,
                })
    
    handler = POIHandler()
    handler.apply_file(str(pbf_path), locations=True)
    
    print(f"  Total nodes scanned: {handler.count:,}")
    print(f"  Relevant POIs extracted: {len(handler.pois):,}")
    
    return handler.pois


def parse_osm_json_fallback(data_dir: str) -> list:
    """Fallback: parse POIs from a preprocessed JSON file if .pbf is unavailable."""
    json_path = Path(data_dir) / "gujarat_pois.json"
    if not json_path.exists():
        return []
    
    print(f"  Loading preprocessed POIs from: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


async def enable_postgis(engine):
    """Ensure PostGIS and pgvector extensions are enabled."""
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    print("  PostGIS + pgvector extensions enabled")


async def ingest_osm(pbf_path: str, data_dir: str, dry_run: bool = False):
    """Main ingestion function."""
    print("=" * 60)
    print("ThinkForge — OpenStreetMap POI Ingestion (Gujarat)")
    print("=" * 60)
    
    # Try .pbf first, fallback to JSON
    pbf_file = Path(pbf_path)
    if pbf_file.exists():
        pois = parse_osm_pbf(str(pbf_file))
    else:
        print(f"  PBF file not found at: {pbf_file}")
        pois = parse_osm_json_fallback(data_dir)
    
    if not pois:
        print("  No POIs found. Please download the Gujarat OSM data:")
        print("    curl -O https://download.geofabrik.de/asia/india/gujarat-latest.osm.pbf")
        print(f"    Move it to: {pbf_path}")
        return
    
    # Print category distribution
    from collections import Counter
    cat_counts = Counter(p["poi_category"] for p in pois)
    print("\n  POI Category Distribution:")
    for cat, count in cat_counts.most_common():
        print(f"    {cat:20s}: {count:,}")
    
    if dry_run:
        print("\n--- DRY RUN (no DB writes) ---")
        for p in pois[:5]:
            print(f"  {p['poi_category']:15s} | {p.get('name', 'unnamed'):30s} | ({p['latitude']:.4f}, {p['longitude']:.4f})")
        return
    
    # Insert into database
    engine = get_engine()
    await enable_postgis(engine)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as db:
        inserted = 0
        batch_size = 500
        
        for i in range(0, len(pois), batch_size):
            batch = pois[i:i + batch_size]
            for poi_dict in batch:
                lat = poi_dict["latitude"]
                lon = poi_dict["longitude"]
                
                # Check duplicate by osm_id
                existing = await db.execute(
                    select(OSMPointOfInterest).where(
                        OSMPointOfInterest.osm_id == poi_dict["osm_id"]
                    )
                )
                if existing.scalar_one_or_none():
                    continue
                
                poi = OSMPointOfInterest(
                    osm_id=poi_dict["osm_id"],
                    name=poi_dict.get("name"),
                    poi_category=poi_dict["poi_category"],
                    amenity=poi_dict.get("amenity"),
                    shop=poi_dict.get("shop"),
                    latitude=lat,
                    longitude=lon,
                    geom=f"SRID=4326;POINT({lon} {lat})",
                    state=poi_dict.get("state", "Gujarat"),
                    district=poi_dict.get("district"),
                    raw_tags=poi_dict.get("raw_tags"),
                )
                db.add(poi)
                inserted += 1
            
            await db.commit()
            print(f"    Batch {i // batch_size + 1}: committed {min(batch_size, len(batch))} POIs")
        
        print(f"\n  DONE: Inserted {inserted} POIs into osm_pois table")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest Gujarat OSM POIs into PostGIS")
    parser.add_argument("--pbf-file", default="data/raw/osm/gujarat-latest.osm.pbf", help="Path to .osm.pbf file")
    parser.add_argument("--data-dir", default="data/raw/osm", help="Fallback directory for preprocessed JSON")
    parser.add_argument("--dry-run", action="store_true", help="Parse without DB writes")
    args = parser.parse_args()
    
    asyncio.run(ingest_osm(args.pbf_file, args.data_dir, dry_run=args.dry_run))
