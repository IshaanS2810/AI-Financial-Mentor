from typing import List, Optional
from pydantic import BaseModel


class RecommendationItem(BaseModel):
    id: str
    title: str
    category: str
    priority: str
    reason: str
    explanation: str
    suggested_action: str


class FinancialSummaryData(BaseModel):
    monthly_income: float
    monthly_expenses: float
    monthly_savings: float
    savings_rate: float
    investment_capacity: float
    emergency_fund: float
    estimated_emergency_months: float
    investment_readiness: str
    investment_readiness_explanation: str


class InvestorProfileData(BaseModel):
    age: Optional[int] = None
    risk_tolerance: str
    investment_horizon: str
    financial_goal: str
    emergency_fund: float
    risk_behavior: Optional[str] = None


class PersonalizedRecommendationsResponse(BaseModel):
    financial_summary: FinancialSummaryData
    profile: Optional[InvestorProfileData] = None
    recommendations: List[RecommendationItem]
