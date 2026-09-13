from typing import Optional
from sqlalchemy.orm import Session

from app.models.financial_profile import FinancialProfile
from app.models.user import User
from app.schemas.financial_profile import FinancialProfileCreate, FinancialProfileUpdate


def get_financial_profile(
    db: Session,
    current_user: User
) -> Optional[FinancialProfile]:
    """Retrieves the financial profile belonging exclusively to the authenticated user."""
    return (
        db.query(FinancialProfile)
        .filter(FinancialProfile.user_id == current_user.id)
        .first()
    )


def create_or_update_financial_profile(
    profile_data: FinancialProfileCreate,
    db: Session,
    current_user: User
) -> FinancialProfile:
    """Creates a new financial profile or updates the existing one for the current user."""
    existing_profile = get_financial_profile(db, current_user)

    if existing_profile:
        existing_profile.age = profile_data.age
        existing_profile.risk_tolerance = profile_data.risk_tolerance
        existing_profile.investment_horizon = profile_data.investment_horizon
        existing_profile.financial_goal = profile_data.financial_goal
        existing_profile.emergency_fund = profile_data.emergency_fund
        existing_profile.risk_behavior = profile_data.risk_behavior

        db.commit()
        db.refresh(existing_profile)
        return existing_profile

    new_profile = FinancialProfile(
        user_id=current_user.id,
        age=profile_data.age,
        risk_tolerance=profile_data.risk_tolerance,
        investment_horizon=profile_data.investment_horizon,
        financial_goal=profile_data.financial_goal,
        emergency_fund=profile_data.emergency_fund,
        risk_behavior=profile_data.risk_behavior,
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile
