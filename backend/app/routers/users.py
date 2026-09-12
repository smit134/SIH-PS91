from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.future import select
import uuid

from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.profile import Profile, RiskTolerance
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

class AuthRequest(BaseModel):
    phone: str = Field(..., description="Phone number to authenticate with")

class AuthResponse(BaseModel):
    user_id: str
    is_new: bool
    has_profile: bool
    name: str | None = None

@router.post("/auth", response_model=AuthResponse)
async def authenticate_user(request: AuthRequest, db: Session = Depends(get_db)):
    """Simulates a fast session authentication by phone number."""
    # Check if user exists
    result = await db.execute(select(User).where(User.phone == request.phone))
    user = result.scalars().first()
    
    is_new = False
    
    if not user:
        # Create user
        is_new = True
        user = User(
            phone=request.phone,
            hashed_password="mock_hash_for_mvp",
            role=UserRole.ENTREPRENEUR,
            is_active=True,
            is_verified=False
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # Check if profile exists
    result_profile = await db.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result_profile.scalars().first()

    return AuthResponse(
        user_id=str(user.id),
        is_new=is_new,
        has_profile=profile is not None,
        name=profile.full_name if profile else None
    )

@router.post("/{user_id}/profile")
async def save_profile(user_id: str, profile_data: dict, db: Session = Depends(get_db)):
    """Save the entrepreneur profile to DB."""
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    result = await db.execute(select(User).where(User.id == uid))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check existing profile
    result_profile = await db.execute(select(Profile).where(Profile.user_id == uid))
    existing = result_profile.scalars().first()
    
    # Parse capital securely (strip ₹ and ,)
    # The frontend is sending the raw UI object directly from the Register wizard
    try:
        capital_str = str(profile_data.get("ownEquity", "0"))
        capital = int(''.join(filter(str.isdigit, capital_str)))
    except:
        capital = 150000

    exp_str = str(profile_data.get("experienceYears", "0"))
    if "Beginner" in exp_str: exp = 1
    elif "1 - 3" in exp_str: exp = 2
    elif "4 - 7" in exp_str: exp = 5
    elif "8+" in exp_str: exp = 8
    else: exp = 0

    if existing:
        existing.available_capital = capital
        existing.experience_years = exp
        existing.approx_location_name = profile_data.get("district", "Unknown")
        await db.commit()
        await db.refresh(existing)
        return {"status": "updated", "profile_id": str(existing.id)}
    else:
        new_profile = Profile(
            user_id=uid,
            full_name=profile_data.get("name", "Rural Entrepreneur"),
            approx_location_name=profile_data.get("district", "Unknown"),
            available_capital=capital,
            experience_years=exp,
            risk_tolerance=RiskTolerance.MEDIUM,
            service_radius_km=15
        )
        db.add(new_profile)
        await db.commit()
        await db.refresh(new_profile)
        return {"status": "created", "profile_id": str(new_profile.id)}
