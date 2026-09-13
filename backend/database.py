"""Backward-compatibility bridge for database.py (used by test_llm.py and scripts)."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.core.database import Base

# Format synchronous URL from asyncpg URL
sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
# Fallback to standard postgresql:// if psycopg2 is default driver
try:
    engine = create_engine(sync_url, pool_pre_ping=True)
    engine.connect().close()
except Exception:
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(sync_url, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
