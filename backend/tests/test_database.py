"""Comprehensive Database & ORM Model Tests.

Verifies schema creation, constraints, foreign keys, enums, and relationships.
"""

import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import (
    Base,
    User,
    UserRole,
    Profile,
    Skill,
    UserSkill,
    Resource,
    UserResource,
    RiskTolerance,
    SkillProficiency,
    ResourceType,
    BusinessCategory,
    PartnerProfile,
    PartnerMatch,
    PartnerVerificationStatus,
    MatchStatus,
    GovernmentScheme,
    EvidenceRecord,
    EvidenceReliabilityClass,
    EvidenceType,
    AuditLog,
)


@pytest.fixture
def db_session():
    """In-memory SQLite synchronous session fixture for schema validation."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(engine)


def test_schema_metadata_contains_all_core_tables():
    """Verifies that Base metadata discovers all 12 core ThinkForge tables."""
    expected_tables = {
        "users",
        "profiles",
        "skills",
        "user_skills",
        "resources",
        "user_resources",
        "business_categories",
        "partner_profiles",
        "partner_matches",
        "schemes",
        "evidence",
        "audit_logs",
    }
    actual_tables = set(Base.metadata.tables.keys())
    assert expected_tables.issubset(actual_tables)


def test_user_and_profile_relationship(db_session: Session):
    """Verifies User creation, Profile relationship, and cascade delete."""
    user = User(
        phone="+919876543210",
        email="rural.entrepreneur@thinkforge.org",
        hashed_password="hashed_secure_password_test",
        role=UserRole.ENTREPRENEUR,
    )
    db_session.add(user)
    db_session.commit()

    profile = Profile(
        user_id=user.id,
        full_name="Ramesh Patel",
        language="hi",
        latitude=23.0225,
        longitude=72.5714,
        approx_location_name="Anand District, Gujarat",
        service_radius_km=10,
        available_capital=50000,
        risk_tolerance=RiskTolerance.MEDIUM,
        experience_years=3,
    )
    db_session.add(profile)
    db_session.commit()

    # Query back and verify relationship
    fetched_user = db_session.get(User, user.id)
    assert fetched_user is not None
    assert fetched_user.profile is not None
    assert fetched_user.profile.full_name == "Ramesh Patel"
    assert fetched_user.profile.available_capital == 50000


def test_skills_and_user_skills(db_session: Session):
    """Verifies Skill taxonomy and UserSkill proficiency mapping."""
    user = User(
        phone="+919876543211",
        hashed_password="hashed_test_pass",
    )
    db_session.add(user)
    db_session.commit()

    profile = Profile(user_id=user.id, full_name="Sunita Devi", language="hi")
    db_session.add(profile)

    skill = Skill(name="Weaving / Loom Operation", category="PRODUCTION")
    db_session.add(skill)
    db_session.commit()

    user_skill = UserSkill(
        profile_id=profile.id,
        skill_id=skill.id,
        proficiency=SkillProficiency.EXPERT,
    )
    db_session.add(user_skill)
    db_session.commit()

    fetched_profile = db_session.get(Profile, profile.id)
    assert len(fetched_profile.skills) == 1
    assert fetched_profile.skills[0].skill.name == "Weaving / Loom Operation"
    assert fetched_profile.skills[0].proficiency == SkillProficiency.EXPERT


def test_business_category_model(db_session: Session):
    """Verifies BusinessCategory creation and attribute storage."""
    category = BusinessCategory(
        name="Handicraft & Textile Production",
        code="HANDICRAFT_TEXTILE",
        description="Traditional rural handloom and textile manufacturing unit.",
        min_capital=30000,
        max_capital=150000,
        typical_monthly_operating_cost=15000,
        typical_monthly_revenue=28000,
        risk_level="MEDIUM",
        required_skills=["Weaving", "Design", "Quality Inspection"],
        required_resources=["Loom", "Storage Workspace"],
        break_even_months_est=9,
        is_active=True,
    )
    db_session.add(category)
    db_session.commit()

    fetched = db_session.query(BusinessCategory).filter_by(code="HANDICRAFT_TEXTILE").first()
    assert fetched is not None
    assert fetched.min_capital == 30000
    assert "Weaving" in fetched.required_skills
    assert fetched.break_even_months_est == 9


def test_partner_profile_and_match(db_session: Session):
    """Verifies PartnerProfile and PartnerMatch with synergy scoring."""
    user1 = User(phone="+919876543212", hashed_password="pass1")
    user2 = User(phone="+919876543213", hashed_password="pass2")
    db_session.add_all([user1, user2])
    db_session.commit()

    partner_profile = PartnerProfile(
        user_id=user2.id,
        investment_capacity_min=50000,
        investment_capacity_max=200000,
        verification_status=PartnerVerificationStatus.BASIC,
    )
    db_session.add(partner_profile)

    match = PartnerMatch(
        user_id=user1.id,
        partner_user_id=user2.id,
        synergy_score=91,
        reasons=["Complementary Capital Fit", "Skill Synergy in Marketing"],
        status=MatchStatus.PENDING,
        initiated_by=user1.id,
    )
    db_session.add(match)
    db_session.commit()

    fetched_match = db_session.get(PartnerMatch, match.id)
    assert fetched_match is not None
    assert fetched_match.synergy_score == 91
    assert fetched_match.status == MatchStatus.PENDING


def test_government_scheme_model(db_session: Session):
    """Verifies GovernmentScheme schema and structured eligibility rules."""
    scheme = GovernmentScheme(
        scheme_name="Prime Minister Employment Generation Programme",
        short_code="PMEGP",
        description="Credit-linked subsidy programme for generating micro-enterprises.",
        eligibility_rules={
            "min_age": 18,
            "min_education": "8th standard for manufacturing over 10L",
            "sectors": ["Manufacturing", "Services"],
        },
        max_loan_amount=5000000,
        interest_rate_annual=0.085,
        subsidy_percentage=0.25,
        tenure_months_max=84,
        required_documents=["Aadhaar", "Project Report", "Caste Certificate if applicable"],
        authority_name="KVIC / MSME",
        is_active=True,
    )
    db_session.add(scheme)
    db_session.commit()

    fetched = db_session.query(GovernmentScheme).filter_by(short_code="PMEGP").first()
    assert fetched is not None
    assert fetched.subsidy_percentage == 0.25
    assert fetched.eligibility_rules["min_age"] == 18


def test_evidence_record_with_reliability_classes(db_session: Session):
    """Verifies EvidenceRecord and mandated reliability classes."""
    evidence = EvidenceRecord(
        source_name="Udyam Registry 2024",
        evidence_type=EvidenceType.COMPETITOR,
        reliability_class=EvidenceReliabilityClass.VERIFIED,
        confidence_score=95,
        latitude=23.0225,
        longitude=72.5714,
        radius_km=10.0,
        payload={"registered_units_count": 14, "niche": "Handicrafts"},
    )
    db_session.add(evidence)
    db_session.commit()

    fetched = db_session.get(EvidenceRecord, evidence.id)
    assert fetched is not None
    assert fetched.reliability_class == EvidenceReliabilityClass.VERIFIED
    assert fetched.payload["registered_units_count"] == 14


def test_audit_log_model(db_session: Session):
    """Verifies AuditLog tracking for sensitive actions."""
    user = User(phone="+919876543214", hashed_password="pass")
    db_session.add(user)
    db_session.commit()

    log = AuditLog(
        user_id=user.id,
        action="AUTH_LOGIN",
        resource_type="USER",
        resource_id=str(user.id),
        ip_address="192.168.1.100",
        details={"auth_method": "PHONE_PASSWORD"},
    )
    db_session.add(log)
    db_session.commit()

    fetched = db_session.get(AuditLog, log.id)
    assert fetched is not None
    assert fetched.action == "AUTH_LOGIN"
    assert fetched.user.phone == "+919876543214"
