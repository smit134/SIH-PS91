"""initial core schema

Revision ID: 20260911_000000
Revises: 
Create Date: 2026-09-11 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260911_000000'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('ENTREPRENEUR', 'ADVISOR', 'ADMIN', name='user_role_enum', native_enum=False), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('users_pkey'))
    )
    op.create_index(op.f('users_phone_idx'), 'users', ['phone'], unique=True)
    op.create_index(op.f('users_email_idx'), 'users', ['email'], unique=True)

    # Profiles table
    op.create_table(
        'profiles',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('language', sa.String(length=10), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('approx_location_name', sa.String(length=255), nullable=True),
        sa.Column('service_radius_km', sa.Integer(), nullable=False),
        sa.Column('available_capital', sa.BigInteger(), nullable=False),
        sa.Column('risk_tolerance', sa.Enum('LOW', 'MEDIUM', 'HIGH', name='risk_tolerance_enum', native_enum=False), nullable=False),
        sa.Column('experience_years', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('profiles_user_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('profiles_pkey')),
        sa.UniqueConstraint('user_id', name=op.f('profiles_user_id_key'))
    )
    op.create_index(op.f('profiles_user_id_idx'), 'profiles', ['user_id'], unique=False)

    # Skills table
    op.create_table(
        'skills',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('skills_pkey'))
    )
    op.create_index(op.f('skills_name_idx'), 'skills', ['name'], unique=True)
    op.create_index(op.f('skills_category_idx'), 'skills', ['category'], unique=False)

    # User Skills table
    op.create_table(
        'user_skills',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('profile_id', sa.Uuid(), nullable=False),
        sa.Column('skill_id', sa.Uuid(), nullable=False),
        sa.Column('proficiency', sa.Enum('BEGINNER', 'INTERMEDIATE', 'EXPERT', name='skill_proficiency_enum', native_enum=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], name=op.f('user_skills_profile_id_fkey'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], name=op.f('user_skills_skill_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('user_skills_pkey'))
    )
    op.create_index(op.f('user_skills_profile_id_idx'), 'user_skills', ['profile_id'], unique=False)
    op.create_index(op.f('user_skills_skill_id_idx'), 'user_skills', ['skill_id'], unique=False)

    # Resources table
    op.create_table(
        'resources',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('resource_type', sa.Enum('LAND', 'EQUIPMENT', 'VEHICLE', 'STORAGE', 'RAW_MATERIAL', 'SHOP', name='resource_type_enum', native_enum=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('resources_pkey'))
    )
    op.create_index(op.f('resources_name_idx'), 'resources', ['name'], unique=True)
    op.create_index(op.f('resources_resource_type_idx'), 'resources', ['resource_type'], unique=False)

    # User Resources table
    op.create_table(
        'user_resources',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('profile_id', sa.Uuid(), nullable=False),
        sa.Column('resource_id', sa.Uuid(), nullable=False),
        sa.Column('details', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], name=op.f('user_resources_profile_id_fkey'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['resource_id'], ['resources.id'], name=op.f('user_resources_resource_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('user_resources_pkey'))
    )
    op.create_index(op.f('user_resources_profile_id_idx'), 'user_resources', ['profile_id'], unique=False)
    op.create_index(op.f('user_resources_resource_id_idx'), 'user_resources', ['resource_id'], unique=False)

    # Business Categories table
    op.create_table(
        'business_categories',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('min_capital', sa.BigInteger(), nullable=False),
        sa.Column('max_capital', sa.BigInteger(), nullable=False),
        sa.Column('typical_monthly_operating_cost', sa.BigInteger(), nullable=False),
        sa.Column('typical_monthly_revenue', sa.BigInteger(), nullable=False),
        sa.Column('risk_level', sa.String(length=20), nullable=False),
        sa.Column('required_skills', sa.JSON(), nullable=False),
        sa.Column('required_resources', sa.JSON(), nullable=False),
        sa.Column('break_even_months_est', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('business_categories_pkey')),
        sa.UniqueConstraint('name', name=op.f('business_categories_name_key'))
    )
    op.create_index(op.f('business_categories_code_idx'), 'business_categories', ['code'], unique=True)

    # Partner Profiles table
    op.create_table(
        'partner_profiles',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('investment_capacity_min', sa.BigInteger(), nullable=False),
        sa.Column('investment_capacity_max', sa.BigInteger(), nullable=False),
        sa.Column('verification_status', sa.Enum('BASIC', 'VERIFIED', name='partner_verification_enum', native_enum=False), nullable=False),
        sa.Column('is_looking_for_partner', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('partner_profiles_user_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('partner_profiles_pkey')),
        sa.UniqueConstraint('user_id', name=op.f('partner_profiles_user_id_key'))
    )
    op.create_index(op.f('partner_profiles_user_id_idx'), 'partner_profiles', ['user_id'], unique=False)

    # Partner Matches table
    op.create_table(
        'partner_matches',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('partner_user_id', sa.Uuid(), nullable=False),
        sa.Column('synergy_score', sa.Integer(), nullable=False),
        sa.Column('reasons', sa.JSON(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'ACCEPTED', 'REJECTED', name='match_status_enum', native_enum=False), nullable=False),
        sa.Column('initiated_by', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['initiated_by'], ['users.id'], name=op.f('partner_matches_initiated_by_fkey'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['partner_user_id'], ['users.id'], name=op.f('partner_matches_partner_user_id_fkey'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('partner_matches_user_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('partner_matches_pkey'))
    )
    op.create_index(op.f('partner_matches_partner_user_id_idx'), 'partner_matches', ['partner_user_id'], unique=False)
    op.create_index(op.f('partner_matches_user_id_idx'), 'partner_matches', ['user_id'], unique=False)

    # Schemes table
    op.create_table(
        'schemes',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('scheme_name', sa.String(length=150), nullable=False),
        sa.Column('short_code', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('eligibility_rules', sa.JSON(), nullable=False),
        sa.Column('max_loan_amount', sa.BigInteger(), nullable=False),
        sa.Column('interest_rate_annual', sa.Float(), nullable=False),
        sa.Column('subsidy_percentage', sa.Float(), nullable=False),
        sa.Column('tenure_months_max', sa.Integer(), nullable=False),
        sa.Column('required_documents', sa.JSON(), nullable=False),
        sa.Column('official_source_url', sa.String(length=255), nullable=True),
        sa.Column('authority_name', sa.String(length=100), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('schemes_pkey')),
        sa.UniqueConstraint('scheme_name', name=op.f('schemes_scheme_name_key'))
    )
    op.create_index(op.f('schemes_short_code_idx'), 'schemes', ['short_code'], unique=True)

    # Evidence table
    op.create_table(
        'evidence',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('source_name', sa.String(length=100), nullable=False),
        sa.Column('evidence_type', sa.Enum('PRICE', 'COMPETITOR', 'DEMAND', 'INFRASTRUCTURE', 'DEMOGRAPHIC', name='evidence_type_enum', native_enum=False), nullable=False),
        sa.Column('reliability_class', sa.Enum('VERIFIED', 'DERIVED', 'ESTIMATED', 'UNKNOWN', name='evidence_reliability_enum', native_enum=False), nullable=False),
        sa.Column('confidence_score', sa.Integer(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('radius_km', sa.Float(), nullable=True),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('fetched_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('evidence_pkey'))
    )
    op.create_index(op.f('evidence_evidence_type_idx'), 'evidence', ['evidence_type'], unique=False)
    op.create_index(op.f('evidence_reliability_class_idx'), 'evidence', ['reliability_class'], unique=False)
    op.create_index(op.f('evidence_source_name_idx'), 'evidence', ['source_name'], unique=False)

    # Audit Logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('resource_type', sa.String(length=50), nullable=False),
        sa.Column('resource_id', sa.String(length=100), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('details', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('audit_logs_user_id_fkey'), ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id', name=op.f('audit_logs_pkey'))
    )
    op.create_index(op.f('audit_logs_action_idx'), 'audit_logs', ['action'], unique=False)
    op.create_index(op.f('audit_logs_resource_type_idx'), 'audit_logs', ['resource_type'], unique=False)
    op.create_index(op.f('audit_logs_user_id_idx'), 'audit_logs', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('audit_logs_user_id_idx'), table_name='audit_logs')
    op.drop_index(op.f('audit_logs_resource_type_idx'), table_name='audit_logs')
    op.drop_index(op.f('audit_logs_action_idx'), table_name='audit_logs')
    op.drop_table('audit_logs')

    op.drop_index(op.f('evidence_source_name_idx'), table_name='evidence')
    op.drop_index(op.f('evidence_reliability_class_idx'), table_name='evidence')
    op.drop_index(op.f('evidence_evidence_type_idx'), table_name='evidence')
    op.drop_table('evidence')

    op.drop_index(op.f('schemes_short_code_idx'), table_name='schemes')
    op.drop_table('schemes')

    op.drop_index(op.f('partner_matches_user_id_idx'), table_name='partner_matches')
    op.drop_index(op.f('partner_matches_partner_user_id_idx'), table_name='partner_matches')
    op.drop_table('partner_matches')

    op.drop_index(op.f('partner_profiles_user_id_idx'), table_name='partner_profiles')
    op.drop_table('partner_profiles')

    op.drop_index(op.f('business_categories_code_idx'), table_name='business_categories')
    op.drop_table('business_categories')

    op.drop_index(op.f('user_resources_resource_id_idx'), table_name='user_resources')
    op.drop_index(op.f('user_resources_profile_id_idx'), table_name='user_resources')
    op.drop_table('user_resources')

    op.drop_index(op.f('resources_resource_type_idx'), table_name='resources')
    op.drop_index(op.f('resources_name_idx'), table_name='resources')
    op.drop_table('resources')

    op.drop_index(op.f('user_skills_skill_id_idx'), table_name='user_skills')
    op.drop_index(op.f('user_skills_profile_id_idx'), table_name='user_skills')
    op.drop_table('user_skills')

    op.drop_index(op.f('skills_category_idx'), table_name='skills')
    op.drop_index(op.f('skills_name_idx'), table_name='skills')
    op.drop_table('skills')

    op.drop_index(op.f('profiles_user_id_idx'), table_name='profiles')
    op.drop_table('profiles')

    op.drop_index(op.f('users_email_idx'), table_name='users')
    op.drop_index(op.f('users_phone_idx'), table_name='users')
    op.drop_table('users')
