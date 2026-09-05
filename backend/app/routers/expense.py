from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
)
from app.services.expense_service import (
    create_expense,
    get_user_expenses,
    get_expense,
    update_expense,
    delete_expense,
)
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED
)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_expense(expense, db, current_user)


@router.get(
    "",
    response_model=list[ExpenseResponse]
)
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_expenses(db, current_user)


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse
)
def get_single_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_expense(expense_id, db, current_user)


@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse
)
def update_expense_record(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_expense(
        expense_id,
        expense_data,
        db,
        current_user
    )


@router.delete(
    "/{expense_id}"
)
def delete_expense_record(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_expense(
        expense_id,
        db,
        current_user
    )
