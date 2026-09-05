from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.income import Income
from app.models.expense import Expense
from app.models.user import User


def get_dashboard_summary(db: Session, current_user: User) -> dict:
    total_income = (
        db.query(func.coalesce(func.sum(Income.amount), 0.0))
        .filter(Income.user_id == current_user.id)
        .scalar()
    ) or 0.0

    total_expenses = (
        db.query(func.coalesce(func.sum(Expense.amount), 0.0))
        .filter(Expense.user_id == current_user.id)
        .scalar()
    ) or 0.0

    savings = total_income - total_expenses

    return {
        "total_income": round(float(total_income), 2),
        "total_expenses": round(float(total_expenses), 2),
        "savings": round(float(savings), 2),
    }


def get_category_breakdown(db: Session, current_user: User) -> list[dict]:
    results = (
        db.query(Expense.category, func.sum(Expense.amount))
        .filter(Expense.user_id == current_user.id)
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
        .all()
    )

    total_expense = sum(float(amount) for _, amount in results)

    breakdown = []
    for category, amount in results:
        amount_val = float(amount)
        pct = (amount_val / total_expense * 100.0) if total_expense > 0 else 0.0
        breakdown.append({
            "category": category,
            "amount": round(amount_val, 2),
            "percentage": round(pct, 2)
        })

    return breakdown


def get_monthly_trend(db: Session, current_user: User) -> list[dict]:
    incomes = (
        db.query(Income)
        .filter(Income.user_id == current_user.id)
        .all()
    )
    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == current_user.id)
        .all()
    )

    months_data = defaultdict(lambda: {"income": 0.0, "expenses": 0.0})

    for inc in incomes:
        if inc.date:
            month_key = inc.date.strftime("%Y-%m")
            months_data[month_key]["income"] += float(inc.amount)

    for exp in expenses:
        if exp.date:
            month_key = exp.date.strftime("%Y-%m")
            months_data[month_key]["expenses"] += float(exp.amount)

    sorted_months = sorted(months_data.keys())
    trend = []
    for m in sorted_months:
        inc_val = round(months_data[m]["income"], 2)
        exp_val = round(months_data[m]["expenses"], 2)
        trend.append({
            "month": m,
            "income": inc_val,
            "expenses": exp_val,
            "savings": round(inc_val - exp_val, 2),
        })

    return trend
