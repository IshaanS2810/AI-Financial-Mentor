from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.income import (
    IncomeCreate,
    IncomeUpdate,
    IncomeResponse,
)
from app.services.income_service import (
    create_income,
    get_user_incomes,
    get_income,
    update_income,
    delete_income,
)
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/income",
    tags=["Income"]
)


@router.post(
    "",
    response_model=IncomeResponse,
    status_code=status.HTTP_201_CREATED
)
def add_income(
    income: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_income(income, db, current_user)


@router.get(
    "",
    response_model=list[IncomeResponse]
)
def get_incomes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_incomes(db, current_user)


@router.get(
    "/{income_id}",
    response_model=IncomeResponse
)
def get_single_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_income(income_id, db, current_user)


@router.put(
    "/{income_id}",
    response_model=IncomeResponse
)
def update_income_record(
    income_id: int,
    income_data: IncomeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_income(
        income_id,
        income_data,
        db,
        current_user
    )


@router.delete(
    "/{income_id}"
)
def delete_income_record(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_income(
        income_id,
        db,
        current_user
    )