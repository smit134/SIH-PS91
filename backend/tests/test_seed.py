"""Unit tests for benchmark business categories and government schemes database seeding."""

import pytest
from sqlalchemy import select
from app.models.business import BusinessCategoryModel
from app.models.scheme import GovernmentScheme
from app.seed.seed_data import seed_business_categories, seed_government_schemes, seed_all


@pytest.mark.anyio
async def test_seed_business_categories(test_db_session):
    """Verifies that the 5 benchmark business categories are inserted idempotently."""
    await seed_business_categories(test_db_session)

    # Verify categories exist
    res = await test_db_session.execute(select(BusinessCategoryModel))
    categories = res.scalars().all()
    codes = [c.code for c in categories]
    assert len(codes) >= 5
    assert "HANDICRAFT" in codes
    assert "DAIRY" in codes
    assert "FOOD_PROCESSING" in codes
    assert "VERMICOMPOST" in codes
    assert "AGRI_RETAIL_LOGISTICS" in codes

    # Idempotency check: second run should insert 0 duplicates
    count_second = await seed_business_categories(test_db_session)
    assert count_second == 0


@pytest.mark.anyio
async def test_seed_government_schemes(test_db_session):
    """Verifies that government schemes (PMEGP, MUDRA, STAND_UP_INDIA) are seeded."""
    await seed_government_schemes(test_db_session)

    res = await test_db_session.execute(select(GovernmentScheme))
    schemes = res.scalars().all()
    short_codes = [s.short_code for s in schemes]
    assert len(short_codes) >= 3
    assert "PMEGP" in short_codes
    assert "MUDRA" in short_codes
    assert "STAND_UP_INDIA" in short_codes

    # Idempotent re-run
    count_second = await seed_government_schemes(test_db_session)
    assert count_second == 0


@pytest.mark.anyio
async def test_seed_all_orchestrator(test_db_session):
    """Verifies the overall seed_all orchestration function."""
    result = await seed_all(test_db_session)
    assert "business_categories_seeded" in result
    assert "schemes_seeded" in result
