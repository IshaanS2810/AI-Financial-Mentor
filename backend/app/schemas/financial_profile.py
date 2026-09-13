from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

ALLOWED_RISK_TOLERANCES = ["Conservative", "Moderate", "Aggressive"]
ALLOWED_HORIZONS = [
    "Less than 3 years",
    "3–5 years", "3-5 years",
    "5–10 years", "5-10 years",
    "More than 10 years"
]
ALLOWED_GOALS = [
    "Wealth creation",
    "Retirement",
    "Buying a house",
    "Education",
    "Short-term savings",
    "General investing"
]


class FinancialProfileCreate(BaseModel):
    age: Optional[int] = Field(default=None, ge=16, le=120, description="User age between 16 and 120")
    risk_tolerance: str = Field(default="Moderate")
    investment_horizon: str = Field(default="5–10 years")
    financial_goal: str = Field(default="Wealth creation")
    emergency_fund: float = Field(default=0.0, ge=0.0, description="Current approximate emergency savings in INR")
    risk_behavior: Optional[str] = Field(default=None, max_length=100)

    @field_validator("risk_tolerance")
    @classmethod
    def validate_risk(cls, v: str) -> str:
        for opt in ALLOWED_RISK_TOLERANCES:
            if v.strip().lower() == opt.lower():
                return opt
        raise ValueError(f"risk_tolerance must be one of: {ALLOWED_RISK_TOLERANCES}")

    @field_validator("investment_horizon")
    @classmethod
    def validate_horizon(cls, v: str) -> str:
        cleaned = v.strip()
        for opt in ALLOWED_HORIZONS:
            if cleaned.lower() == opt.lower():
                # Standardize to en-dash
                if "3-5" in opt:
                    return "3–5 years"
                if "5-10" in opt:
                    return "5–10 years"
                return opt
        raise ValueError(f"investment_horizon must be one of: {ALLOWED_HORIZONS}")

    @field_validator("financial_goal")
    @classmethod
    def validate_goal(cls, v: str) -> str:
        for opt in ALLOWED_GOALS:
            if v.strip().lower() == opt.lower():
                return opt
        raise ValueError(f"financial_goal must be one of: {ALLOWED_GOALS}")


class FinancialProfileUpdate(BaseModel):
    age: Optional[int] = Field(default=None, ge=16, le=120)
    risk_tolerance: Optional[str] = None
    investment_horizon: Optional[str] = None
    financial_goal: Optional[str] = None
    emergency_fund: Optional[float] = Field(default=None, ge=0.0)
    risk_behavior: Optional[str] = Field(default=None, max_length=100)

    @field_validator("risk_tolerance")
    @classmethod
    def validate_risk(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        for opt in ALLOWED_RISK_TOLERANCES:
            if v.strip().lower() == opt.lower():
                return opt
        raise ValueError(f"risk_tolerance must be one of: {ALLOWED_RISK_TOLERANCES}")

    @field_validator("investment_horizon")
    @classmethod
    def validate_horizon(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        cleaned = v.strip()
        for opt in ALLOWED_HORIZONS:
            if cleaned.lower() == opt.lower():
                if "3-5" in opt:
                    return "3–5 years"
                if "5-10" in opt:
                    return "5–10 years"
                return opt
        raise ValueError(f"investment_horizon must be one of: {ALLOWED_HORIZONS}")

    @field_validator("financial_goal")
    @classmethod
    def validate_goal(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        for opt in ALLOWED_GOALS:
            if v.strip().lower() == opt.lower():
                return opt
        raise ValueError(f"financial_goal must be one of: {ALLOWED_GOALS}")


class FinancialProfileResponse(BaseModel):
    id: int
    user_id: int
    age: Optional[int] = None
    risk_tolerance: str
    investment_horizon: str
    financial_goal: str
    emergency_fund: float
    risk_behavior: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
