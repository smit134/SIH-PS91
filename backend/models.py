from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from database import Base

class Evidence(Base):
    __tablename__ = 'evidence'

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)
    radius_km = Column(Float, nullable=True)
    evidence_type = Column(String, index=True) # e.g. Price, Competitor, Demand
    content = Column(Text, nullable=False)
    confidence = Column(Integer, default=100)
    embedding = Column(Vector(768)) # Default size for nomic-embed-text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
