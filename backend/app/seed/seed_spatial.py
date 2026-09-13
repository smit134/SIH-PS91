import asyncio
import os
import uuid
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement
import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_URL = "postgresql://thinkforge:thinkforge_dev_password@localhost:5432/thinkforge"
engine = create_engine(DB_URL)
DATA_DIR = r"c:\Users\smit\OneDrive\Desktop\Programing Journey\SIH-91\backend\app\data"

def seed_overture():
    path = os.path.join(DATA_DIR, "gujarat_businesses.parquet")
    logger.info(f"Loading {path}...")
    
    gdf = gpd.read_parquet(path)
    logger.info(f"Loaded {len(gdf)} records.")
    
    gdf['poi_id'] = gdf['id'].astype(str)
    gdf['name'] = gdf['names'].apply(lambda x: x.get('primary') if isinstance(x, dict) else None)
    gdf['category'] = gdf['categories'].apply(lambda x: x.get('primary') if isinstance(x, dict) else None)
    gdf['confidence'] = gdf.get('confidence', None)
    
    gdf['latitude'] = gdf.geometry.y
    gdf['longitude'] = gdf.geometry.x
    
    insert_df = gdf[['poi_id', 'name', 'category', 'confidence', 'latitude', 'longitude', 'geometry']]
    insert_df = insert_df.set_geometry('geometry')
    
    # Manually add Base model fields since we rely on to_postgis to create the table
    insert_df['id'] = [str(uuid.uuid4()) for _ in range(len(insert_df))]
    now = datetime.now(timezone.utc)
    insert_df['created_at'] = now
    insert_df['updated_at'] = now
    
    logger.info("Inserting into business_poi...")
    # Use to_postgis which creates the table if it doesn't exist
    insert_df.to_postgis("business_poi", engine, if_exists='replace', index=False, chunksize=10000)
    logger.info("Business points inserted.")


def seed_kontur():
    path = os.path.join(DATA_DIR, "gujarat_population.gpkg")
    logger.info(f"Loading {path}...")
    gdf = gpd.read_file(path)
    logger.info(f"Loaded {len(gdf)} records.")
    
    gdf['population'] = gdf['population'].astype(int)
    insert_df = gdf[['population', 'geometry']]
    insert_df['id'] = [str(uuid.uuid4()) for _ in range(len(insert_df))]
    now = datetime.now(timezone.utc)
    insert_df['created_at'] = now
    insert_df['updated_at'] = now
    
    logger.info("Inserting into population_grid...")
    insert_df.to_postgis("population_grid", engine, if_exists='replace', index=False, chunksize=10000)
    logger.info("Population grid inserted.")

if __name__ == "__main__":
    try:
        seed_overture()
    except Exception as e:
        logger.error(f"Error seeding Overture: {e}")
    
    try:
        seed_kontur()
    except Exception as e:
        logger.error(f"Error seeding Kontur: {e}")

    logger.info("Spatial data seeding completed successfully.")
