"""Database Seeding Script for Benchmark Business Categories and Schemes."""

import json
from pathlib import Path
from typing import Dict, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import BusinessCategory
from app.models.scheme import GovernmentScheme

SEED_DIR = Path(__file__).parent


async def seed_business_categories(db: AsyncSession) -> int:
    """Seeds the 5 foundational benchmark rural business categories."""
    json_path = SEED_DIR / "categories_seed.json"
    with open(json_path, "r", encoding="utf-8") as f:
        categories_data = json.load(f)

    inserted_count = 0
    for cat_dict in categories_data:
        existing = await db.execute(
            select(BusinessCategory).where(BusinessCategory.code == cat_dict["code"])
        )
        if not existing.scalar_one_or_none():
            category = BusinessCategory(**cat_dict)
            db.add(category)
            inserted_count += 1

    if inserted_count > 0:
        await db.commit()
    return inserted_count


async def seed_government_schemes(db: AsyncSession) -> int:
    """Seeds essential government financing schemes for rural micro-enterprises."""
    schemes_data = [
        {
            "scheme_name": "Prime Minister Employment Generation Programme",
            "short_code": "PMEGP",
            "description": "Credit-linked subsidy programme aiming to generate self-employment opportunities through micro-enterprise ventures in rural and urban areas.",
            "eligibility_rules": {
                "min_age": 18,
                "min_education": "8th standard for project cost above 10L in manufacturing",
                "target_sectors": ["Manufacturing", "Services", "Agro-Processing"],
            },
            "max_loan_amount": 5000000,
            "interest_rate_annual": 0.085,
            "subsidy_percentage": 0.35,  # Up to 35% in rural areas
            "tenure_months_max": 84,
            "required_documents": ["Aadhaar", "Project Report", "Skill/EDP Certificate", "Rural Area Certificate"],
            "official_source_url": "https://www.kviconline.gov.in/pmegpeportal",
            "authority_name": "Ministry of MSME / KVIC",
            "is_active": True,
        },
        {
            "scheme_name": "Pradhan Mantri MUDRA Yojana (Shishu & Kishore)",
            "short_code": "MUDRA",
            "description": "Collateral-free institutional credit to micro/small business units up to Rs. 5 Lakhs (Shishu: up to 50k, Kishore: 50k to 5L).",
            "eligibility_rules": {
                "min_age": 18,
                "target_sectors": ["Non-Farm Enterprise", "Artisans", "Small Shopkeepers", "Agri-Allied"],
            },
            "max_loan_amount": 500000,
            "interest_rate_annual": 0.09,
            "subsidy_percentage": 0.0,  # Interest subvention, no upfront capital subsidy
            "tenure_months_max": 60,
            "required_documents": ["Aadhaar", "Bank Account Statement", "Business Proof / Quotations"],
            "official_source_url": "https://www.mudra.org.in",
            "authority_name": "Department of Financial Services / MUDRA",
            "is_active": True,
        },
        {
            "scheme_name": "Stand-Up India Scheme",
            "short_code": "STAND_UP_INDIA",
            "description": "Bank loans between 10 Lakhs and 1 Crore to at least one SC or ST borrower and at least one woman borrower per bank branch.",
            "eligibility_rules": {
                "min_age": 18,
                "target_groups": ["SC", "ST", "Women"],
                "enterprise_type": "Greenfield Enterprise",
            },
            "max_loan_amount": 10000000,
            "interest_rate_annual": 0.0825,
            "subsidy_percentage": 0.15,
            "tenure_months_max": 84,
            "required_documents": ["Identity Proof", "Caste Certificate if applicable", "Project Report", "Pollution Clearance"],
            "official_source_url": "https://www.standupmitra.in",
            "authority_name": "SIDBI / Ministry of Finance",
            "is_active": True,
        },
    ]

    inserted_count = 0
    for scheme_dict in schemes_data:
        existing = await db.execute(
            select(GovernmentScheme).where(GovernmentScheme.short_code == scheme_dict["short_code"])
        )
        if not existing.scalar_one_or_none():
            scheme = GovernmentScheme(**scheme_dict)
            db.add(scheme)
            inserted_count += 1

    if inserted_count > 0:
        await db.commit()
    return inserted_count


async def seed_all(db: AsyncSession) -> Dict[str, int]:
    """Runs all database seeding routines."""
    cats = await seed_business_categories(db)
    schemes = await seed_government_schemes(db)
    return {"business_categories_seeded": cats, "schemes_seeded": schemes}
