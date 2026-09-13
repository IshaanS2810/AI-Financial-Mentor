from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.financial_profile import (
    FinancialProfileCreate,
    FinancialProfileResponse,
)
from app.services.financial_profile_service import (
    get_financial_profile,
    create_or_update_financial_profile,
)
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/profile",
    tags=["Financial Profile"]
)


@router.get(
    "",
    response_model=Optional[FinancialProfileResponse]
)
def get_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_financial_profile(db, current_user)


@router.post(
    "",
    response_model=FinancialProfileResponse,
    status_code=status.HTTP_200_OK
)
def upsert_user_profile(
    profile_data: FinancialProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_or_update_financial_profile(profile_data, db, current_user)
