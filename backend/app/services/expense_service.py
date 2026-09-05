from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


def create_expense(
    expense: ExpenseCreate,
    db: Session,
    current_user: User
):
    new_expense = Expense(
        user_id=current_user.id,
        category=expense.category,
        description=expense.description,
        amount=expense.amount,
        date=expense.date,
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


def get_user_expenses(
    db: Session,
    current_user: User
):
    return (
        db.query(Expense)
        .filter(Expense.user_id == current_user.id)
        .order_by(Expense.date.desc())
        .all()
    )


def get_expense(
    expense_id: int,
    db: Session,
    current_user: User
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == current_user.id
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense record not found"
        )

    return expense


def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session,
    current_user: User
):
    expense = get_expense(expense_id, db, current_user)

    update_data = expense_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)

    return expense


def delete_expense(
    expense_id: int,
    db: Session,
    current_user: User
):
    expense = get_expense(expense_id, db, current_user)

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted successfully"}
