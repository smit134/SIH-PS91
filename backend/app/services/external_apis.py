
import json
import os
import asyncio
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "verified_datasets"

async def fetch_government_schemes():
    """
    Simulates an external API call to Data.gov.in by reading a local static dataset.
    Adds a small synthetic delay to simulate network latency.
    """
    await asyncio.sleep(0.5)  # Simulate network latency
    
    schemes_file = DATA_DIR / "schemes.json"
    if not schemes_file.exists():
        return []
        
    with open(schemes_file, "r") as f:
        return json.load(f)
