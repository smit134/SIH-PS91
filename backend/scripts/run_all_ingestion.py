"""Master Data Ingestion Runner — runs all dataset ingestion scripts in order.

Usage:
    python -m scripts.run_all_ingestion [--dry-run] [--skip-osm] [--skip-pdf]
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text
from app.core.database import get_engine, Base


async def setup_extensions():
    """Enable PostGIS and pgvector extensions."""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        print("  ✅ PostGIS + pgvector extensions enabled")


async def create_tables():
    """Create all new tables."""
    engine = get_engine()
    
    # Import all models to register them
    import app.models  # noqa: F401
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("  ✅ All database tables created/verified")


async def run_all(dry_run=False, skip_osm=False, skip_pdf=False):
    """Run all ingestion scripts in sequence."""
    print("=" * 70)
    print("  ThinkForge — Master Data Ingestion Pipeline")
    print("=" * 70)
    
    # Step 0: Database setup
    print("\n📦 Step 0: Database Setup")
    await setup_extensions()
    await create_tables()
    
    # Step 1: Government Schemes
    print("\n📋 Step 1: Government Schemes (Kaggle MyScheme)")
    from scripts.ingest_schemes import ingest_schemes
    await ingest_schemes("data/raw/schemes", dry_run=dry_run)
    
    # Step 2: Financial Templates
    print("\n💰 Step 2: MSME Financial Templates")
    from scripts.build_financial_templates import main as build_fin
    build_fin()  # This is synchronous
    
    # Step 3: District MSME Stats
    print("\n🏘️ Step 3: District MSME Statistics (Gujarat)")
    from scripts.ingest_district_msme import ingest_district_msme
    await ingest_district_msme("data/raw/district_msme", dry_run=dry_run)
    
    # Step 4: OSM POIs (optional — requires large .pbf download)
    if not skip_osm:
        print("\n🗺️ Step 4: OpenStreetMap POIs (Gujarat)")
        from scripts.ingest_osm import ingest_osm
        await ingest_osm(
            "data/raw/osm/gujarat-latest.osm.pbf",
            "data/raw/osm",
            dry_run=dry_run,
        )
    else:
        print("\n🗺️ Step 4: Skipped (--skip-osm)")
    
    # Step 5: PDF → pgvector (optional — requires PDF + Gemini API key)
    if not skip_pdf:
        print("\n📄 Step 5: PMEGP/MUDRA PDF → pgvector")
        from scripts.ingest_pdf_to_vectors import ingest_pdf
        
        pmegp_path = "data/raw/pdfs/pmegp_guidelines.pdf"
        if Path(pmegp_path).exists():
            await ingest_pdf(pmegp_path, "PMEGP_Guidelines", dry_run=dry_run)
        else:
            print(f"  ⚠️ PMEGP PDF not found at {pmegp_path}")
            print(f"  Download: curl -o {pmegp_path} https://www.kviconline.gov.in/pmegp/pmegpweb/docs/homepage/PMEGPscheme.pdf")
    else:
        print("\n📄 Step 5: Skipped (--skip-pdf)")
    
    print("\n" + "=" * 70)
    print("  ✅ Master ingestion pipeline complete!")
    print("=" * 70)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run all ThinkForge data ingestion scripts")
    parser.add_argument("--dry-run", action="store_true", help="Parse and validate without DB writes")
    parser.add_argument("--skip-osm", action="store_true", help="Skip OSM POI ingestion (requires .pbf download)")
    parser.add_argument("--skip-pdf", action="store_true", help="Skip PDF vectorization (requires Gemini API key)")
    args = parser.parse_args()
    
    asyncio.run(run_all(dry_run=args.dry_run, skip_osm=args.skip_osm, skip_pdf=args.skip_pdf))
