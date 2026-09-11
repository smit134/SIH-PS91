import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine, SessionLocal, Base
from models import Evidence
from services.llm_service import llm_service

def seed():
    # Load mock evidence data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mock_evidence.json')
    if not os.path.exists(data_path):
        print("Mock data file not found.")
        return

    with open(data_path, 'r') as f:
        evidences = json.load(f)

    db = SessionLocal()
    try:
        for item in evidences:
            # Generate embedding using local Ollama
            embedding = llm_service.generate_embedding(item['content'])
            
            db_item = Evidence(
                source=item['source'],
                location_lat=item.get('location_lat'),
                location_lng=item.get('location_lng'),
                radius_km=item.get('radius_km'),
                evidence_type=item['evidence_type'],
                content=item['content'],
                confidence=item.get('confidence', 100),
                embedding=embedding
            )
            db.add(db_item)
        db.commit()
        print(f"Seeded {len(evidences)} evidence records.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
