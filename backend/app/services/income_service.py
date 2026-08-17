from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.user import User
from app.schemas.income import IncomeCreate, IncomeUpdate


def create_income(
    income: IncomeCreate,
    db: Session,
    current_user: User
):
    new_income = Income(
        user_id=current_user.id,
        amount=income.amount,
        source=income.source,
        category=income.category,
        date=income.date,
        description=income.description,
    )

    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    return new_income


def get_user_incomes(
    db: Session,
    current_user: User
):
    return (
        db.query(Income)
        .filter(Income.user_id == current_user.id)
        .order_by(Income.date.desc())
        .all()
    )


def get_income(
    income_id: int,
    db: Session,
    current_user: User
):
    income = (
        db.query(Income)
        .filter(
            Income.id == income_id,
            Income.user_id == current_user.id
        )
        .first()
    )

    if not income:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Income record not found"
        )

    return income


def update_income(
    income_id: int,
    income_data: IncomeUpdate,
    db: Session,
    current_user: User
):
    income = get_income(income_id, db, current_user)

    update_data = income_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(income, field, value)

    db.commit()
    db.refresh(income)

    return income


def delete_income(
    income_id: int,
    db: Session,
    current_user: User
):
    income = get_income(income_id, db, current_user)

    db.delete(income)
    db.commit()

    return {"message": "Income deleted successfully"}