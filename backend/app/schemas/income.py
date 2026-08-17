from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class IncomeCreate(BaseModel):
    amount: float = Field(gt=0)
    source: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=100)
    date: date
    description: Optional[str] = Field(
        default=None,
        max_length=255
    )


class IncomeUpdate(BaseModel):
    amount: Optional[float] = Field(
        default=None,
        gt=0
    )
    source: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
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


class IncomeResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    source: str
    category: str
    date: date
    description: Optional[str]

    model_config = {
        "from_attributes": True
    }