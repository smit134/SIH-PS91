"""Profile Management Router: Capability Profiling, Skills, Assets, and Readiness."""

from typing import Any, List
import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.exceptions import NotFoundException
from app.models.profile import Profile, Resource, Skill, UserResource, UserSkill
from app.models.user import User
from app.schemas.profile import (
    ProfileReadinessResponse,
    ProfileResponse,
    ProfileUpdate,
    ResourceCreate,
    SkillCreate,
    UserResourceResponse,
    UserSkillResponse,
)

router = APIRouter()


async def _get_profile_with_relations(user_id: uuid.UUID, db: AsyncSession) -> Profile:
    """Helper to query profile with eager loaded skills and resources."""
    query = (
        select(Profile)
        .where(Profile.user_id == user_id)
        .options(
            selectinload(Profile.skills).selectinload(UserSkill.skill),
            selectinload(Profile.resources).selectinload(UserResource.resource),
        )
    )
    result = await db.execute(query)
    profile = result.scalar_one_or_none()
    if not profile:
        raise NotFoundException(message="Entrepreneur profile not found.")
    return profile


def _format_profile_response(profile: Profile) -> ProfileResponse:
    """Formats ORM profile into ProfileResponse DTO."""
    skills_dto = [
        UserSkillResponse(
            id=us.id,
            skill_id=us.skill_id,
            name=us.skill.name if us.skill else "Unknown Skill",
            category=us.skill.category if us.skill else "GENERAL",
            proficiency=us.proficiency,
        )
        for us in profile.skills
    ]
    resources_dto = [
        UserResourceResponse(
            id=ur.id,
            resource_id=ur.resource_id,
            name=ur.resource.name if ur.resource else "Unknown Resource",
            resource_type=ur.resource.resource_type if ur.resource else "EQUIPMENT",
            details=ur.details,
        )
        for ur in profile.resources
    ]

    return ProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        full_name=profile.full_name,
        language=profile.language,
        latitude=profile.latitude,
        longitude=profile.longitude,
        approx_location_name=profile.approx_location_name,
        service_radius_km=profile.service_radius_km,
        available_capital=profile.available_capital,
        risk_tolerance=profile.risk_tolerance,
        experience_years=profile.experience_years,
        skills=skills_dto,
        resources=resources_dto,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )


@router.get(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user's capability profile",
)
async def get_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    profile = await _get_profile_with_relations(current_user.id, db)
    return _format_profile_response(profile)


@router.put(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Update entrepreneur capability profile",
)
async def update_profile(
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    profile = await _get_profile_with_relations(current_user.id, db)

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.add(profile)
    await db.commit()
    await db.refresh(profile)

    refetched = await _get_profile_with_relations(current_user.id, db)
    return _format_profile_response(refetched)


@router.post(
    "/skills",
    response_model=UserSkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add or update a skill on the profile",
)
async def add_skill(
    payload: SkillCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    profile = await _get_profile_with_relations(current_user.id, db)

    # Get or create canonical skill
    skill_query = select(Skill).where(Skill.name == payload.name)
    skill_res = await db.execute(skill_query)
    skill = skill_res.scalar_one_or_none()

    if not skill:
        skill = Skill(name=payload.name, category=payload.category)
        db.add(skill)
        await db.flush()

    # Check if profile already has this skill
    user_skill_query = select(UserSkill).where(
        UserSkill.profile_id == profile.id,
        UserSkill.skill_id == skill.id,
    )
    user_skill_res = await db.execute(user_skill_query)
    user_skill = user_skill_res.scalar_one_or_none()

    if user_skill:
        user_skill.proficiency = payload.proficiency
    else:
        user_skill = UserSkill(
            profile_id=profile.id,
            skill_id=skill.id,
            proficiency=payload.proficiency,
        )
        db.add(user_skill)

    await db.commit()
    await db.refresh(user_skill)

    return UserSkillResponse(
        id=user_skill.id,
        skill_id=skill.id,
        name=skill.name,
        category=skill.category,
        proficiency=user_skill.proficiency,
    )


@router.delete(
    "/skills/{skill_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove a skill from the profile",
)
async def remove_skill(
    skill_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    profile = await _get_profile_with_relations(current_user.id, db)
    del_query = delete(UserSkill).where(
        UserSkill.profile_id == profile.id,
        UserSkill.skill_id == skill_id,
    )
    await db.execute(del_query)
    await db.commit()
    return {"success": True, "message": "Skill removed from profile."}


@router.post(
    "/resources",
    response_model=UserResourceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add or update a physical resource on the profile",
)
async def add_resource(
    payload: ResourceCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    profile = await _get_profile_with_relations(current_user.id, db)

    # Get or create canonical resource
    res_query = select(Resource).where(Resource.name == payload.name)
    res_result = await db.execute(res_query)
    resource = res_result.scalar_one_or_none()

    if not resource:
        resource = Resource(name=payload.name, resource_type=payload.resource_type)
        db.add(resource)
        await db.flush()

    user_res_query = select(UserResource).where(
        UserResource.profile_id == profile.id,
        UserResource.resource_id == resource.id,
    )
    user_res_result = await db.execute(user_res_query)
    user_resource = user_res_result.scalar_one_or_none()

    if user_resource:
        user_resource.details = payload.details
    else:
        user_resource = UserResource(
            profile_id=profile.id,
            resource_id=resource.id,
            details=payload.details,
        )
        db.add(user_resource)

    await db.commit()
    await db.refresh(user_resource)

    return UserResourceResponse(
        id=user_resource.id,
        resource_id=resource.id,
        name=resource.name,
        resource_type=resource.resource_type,
        details=user_resource.details,
    )


@router.delete(
    "/resources/{resource_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove a resource from the profile",
)
async def remove_resource(
    resource_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    profile = await _get_profile_with_relations(current_user.id, db)
    del_query = delete(UserResource).where(
        UserResource.profile_id == profile.id,
        UserResource.resource_id == resource_id,
    )
    await db.execute(del_query)
    await db.commit()
    return {"success": True, "message": "Resource removed from profile."}


@router.get(
    "/readiness",
    response_model=ProfileReadinessResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate profile readiness percentage and capability gaps",
)
async def calculate_readiness(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    profile = await _get_profile_with_relations(current_user.id, db)

    score = 0
    completed: List[str] = []
    missing: List[str] = []
    recs: List[str] = []

    # 1. Identity & Language (20%)
    if profile.full_name and len(profile.full_name.strip()) >= 2:
        score += 20
        completed.append("Personal Identity")
    else:
        missing.append("Personal Identity")
        recs.append("Complete your full name and preferred language.")

    # 2. Location & Catchment Radius (20%)
    if profile.latitude is not None and profile.longitude is not None:
        score += 20
        completed.append("Geographic Location")
    else:
        missing.append("Geographic Location")
        recs.append("Set your village or district coordinates to discover nearby opportunities.")

    # 3. Capital & Risk Preferences (20%)
    if profile.available_capital > 0:
        score += 20
        completed.append("Capital & Budget")
    else:
        missing.append("Capital & Budget")
        recs.append("Specify your starting investment budget to receive tailored recommendations.")

    # 4. Skills Inventory (20%)
    if len(profile.skills) > 0:
        score += 20
        completed.append("Skills & Experience")
    else:
        missing.append("Skills & Experience")
        recs.append("List at least one trade or commercial skill you possess.")

    # 5. Physical Assets & Equipment (20%)
    if len(profile.resources) > 0:
        score += 20
        completed.append("Physical Resources")
    else:
        missing.append("Physical Resources")
        recs.append("Add owned physical assets (e.g., land, machinery, shop space) to calculate Resource-Fit.")

    return ProfileReadinessResponse(
        readiness_percentage=score,
        completed_sections=completed,
        missing_sections=missing,
        recommendations=recs,
    )
