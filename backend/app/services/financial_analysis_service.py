from collections import defaultdict
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense
from app.models.user import User
from app.models.financial_profile import FinancialProfile
from app.services.financial_profile_service import get_financial_profile
from app.services.analytics_service import get_category_breakdown


def calculate_user_financial_analysis(
    db: Session,
    current_user: User
) -> Dict[str, Any]:
    """Calculates comprehensive financial diagnostics from actual income and expense records.
    
    Returns deterministic metrics including monthly cashflow, savings rate,
    emergency fund coverage, investment readiness status, and estimated capacity.
    """
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

    # 1. Compute Monthly Distributions
    monthly_incomes = defaultdict(float)
    monthly_expenses = defaultdict(float)

    for inc in incomes:
        if inc.date:
            m_key = inc.date.strftime("%Y-%m")
            monthly_incomes[m_key] += float(inc.amount)

    for exp in expenses:
        if exp.date:
            m_key = exp.date.strftime("%Y-%m")
            monthly_expenses[m_key] += float(exp.amount)

    all_months = set(monthly_incomes.keys()).union(set(monthly_expenses.keys()))
    num_months = len(all_months) if len(all_months) > 0 else 1

    total_income = sum(float(inc.amount) for inc in incomes)
    total_expenses = sum(float(exp.amount) for exp in expenses)

    # Average Monthly Values
    avg_monthly_income = round(total_income / num_months, 2)
    avg_monthly_expenses = round(total_expenses / num_months, 2)
    monthly_savings = round(avg_monthly_income - avg_monthly_expenses, 2)

    # Savings Rate calculation (handled safely for zero income or negative cashflow)
    if avg_monthly_income > 0 and monthly_savings > 0:
        savings_rate = round((monthly_savings / avg_monthly_income) * 100, 2)
    else:
        savings_rate = 0.0

    # 2. Category Breakdown & Top Expenses
    category_breakdown = get_category_breakdown(db, current_user)
    top_categories = category_breakdown[:3]

    # 3. Emergency Fund Analysis
    profile = get_financial_profile(db, current_user)
    emergency_fund = float(profile.emergency_fund) if profile else 0.0

    # Emergency fund months estimate based on monthly expenses as conservative proxy
    if avg_monthly_expenses > 0:
        estimated_emergency_months = round(emergency_fund / avg_monthly_expenses, 1)
    else:
        # If no expenses recorded yet but emergency fund exists
        estimated_emergency_months = 6.0 if emergency_fund > 0 else 0.0

    # 4. Educational Investment Readiness Classification & Capacity Heuristics
    # Rules:
    # - NOT_READY: User has zero income or is operating at a monthly deficit (savings <= 0).
    # - BUILD_EMERGENCY_FUND: User has positive surplus, but emergency fund < 3 months of expenses.
    # - READY_TO_EXPLORE: Emergency fund has 3-6 months coverage and healthy surplus.
    # - STRONG_INVESTMENT_CAPACITY: Emergency fund has >= 6 months coverage and savings rate >= 20%.

    if avg_monthly_income <= 0 or monthly_savings <= 0:
        readiness_status = "NOT_READY"
        investment_capacity = 0.0
        readiness_explanation = (
            "Your recorded finances indicate a monthly deficit or zero income. "
            "Focus on expense reduction and stabilizing positive cashflow before allocating capital to investments."
        )
    elif estimated_emergency_months < 3.0:
        readiness_status = "BUILD_EMERGENCY_FUND"
        # Prioritize emergency savings: allocate only 25% of surplus for education/micro-SIP, keeping 75% for emergency fund
        investment_capacity = round(monthly_savings * 0.25, 2)
        readiness_explanation = (
            f"Your current emergency fund of ₹{emergency_fund:,.0f} covers approximately {estimated_emergency_months} "
            "months of living expenses. Standard guidelines suggest accumulating 3–6 months of living expenses "
            "before committing significant funds to long-term market investments."
        )
    elif estimated_emergency_months < 6.0 or savings_rate < 20.0:
        readiness_status = "READY_TO_EXPLORE"
        # 3-6 months buffer: allocate ~60% of surplus to investments, 40% for ongoing savings
        investment_capacity = round(monthly_savings * 0.60, 2)
        readiness_explanation = (
            f"You have a sound base with ~{estimated_emergency_months} months of emergency coverage and a "
            f"{savings_rate}% savings rate. You appear ready to explore disciplined investments such as monthly SIPs."
        )
    else:
        readiness_status = "STRONG_INVESTMENT_CAPACITY"
        # 6+ months buffer & strong savings rate: can comfortably invest up to 80% of surplus
        investment_capacity = round(monthly_savings * 0.80, 2)
        readiness_explanation = (
            f"Excellent foundation! Your emergency fund covers {estimated_emergency_months} months of living expenses, "
            f"and you maintain a strong {savings_rate}% savings rate. You have solid capacity for diversified long-term wealth creation."
        )

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "monthly_income": avg_monthly_income,
        "monthly_expenses": avg_monthly_expenses,
        "monthly_savings": monthly_savings,
        "savings_rate": savings_rate,
        "emergency_fund": emergency_fund,
        "estimated_emergency_months": estimated_emergency_months,
        "investment_readiness": readiness_status,
        "investment_readiness_explanation": readiness_explanation,
        "investment_capacity": investment_capacity,
        "category_breakdown": category_breakdown,
        "top_categories": top_categories,
        "months_recorded": num_months,
    }
