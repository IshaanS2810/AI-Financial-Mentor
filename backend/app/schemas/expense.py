from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0, description="Amount must be greater than 0")
    category: str = Field(min_length=1, max_length=100)
    date: date
    description: Optional[str] = Field(
        default=None,
        max_length=255
    )


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(
        default=None,
        gt=0
    )
    category: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    date: Optional[date] = None
    description: Optional[str] = Field(
        default=None,
        max_length=255
    )


class ExpenseResponse(BaseModel):
    id: int
    user_id: int
    category: str
    description: Optional[str] = None
    amount: float
    date: date
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
