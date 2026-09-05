from typing import List
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_income: float
    total_expenses: float
    savings: float


class CategoryBreakdownItem(BaseModel):
    category: str
    amount: float
    percentage: float


class MonthlyTrendItem(BaseModel):
    month: str
    income: float
    expenses: float
    savings: float
