"""Pytest Configuration, Shared Test Fixtures, and DB Dependency Overrides."""

import sys
from pathlib import Path
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Ensure backend root is on Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import get_db
from app.main import app
from app.models import Base


class AsyncTestSessionWrapper:
    """Adapts a synchronous SQLite test session to the AsyncSession interface for testing."""

    def __init__(self, sync_session: Session):
        self._s = sync_session

    async def execute(self, statement):
        return self._s.execute(statement)

    def add(self, instance):
        self._s.add(instance)

    def add_all(self, instances):
        self._s.add_all(instances)

    async def flush(self):
        self._s.flush()

    async def commit(self):
        self._s.commit()

    async def rollback(self):
        self._s.rollback()

    async def refresh(self, instance):
        self._s.refresh(instance)

    async def get(self, entity, ident):
        return self._s.get(entity, ident)


@pytest.fixture(scope="session")
def test_engine():
    """In-memory SQLite engine for all test sessions."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    sqlite_tables = [
        t for name, t in Base.metadata.tables.items()
        if name not in ("osm_pois", "scheme_document_chunks")
    ]
    Base.metadata.create_all(engine, tables=sqlite_tables)
    yield engine
    Base.metadata.drop_all(engine, tables=sqlite_tables)


@pytest.fixture
def test_db_session(test_engine):
    """Per-test transactional session wrapper."""
    with Session(test_engine) as session:
        wrapper = AsyncTestSessionWrapper(session)
        yield wrapper
        session.rollback()


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client(test_db_session):
    """Async HTTP test client fixture with overridden database dependency."""

    async def override_get_db():
        yield test_db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(autouse=True)
def mock_sms_gateway(monkeypatch):
    """Prevents live cellular SMS API calls during test suite runs."""
    async def _mock_send(phone: str, otp_code: str):
        return True, f"Mock OTP {otp_code} dispatched to {phone}"

    monkeypatch.setattr("app.core.sms.send_sms_otp", _mock_send)
