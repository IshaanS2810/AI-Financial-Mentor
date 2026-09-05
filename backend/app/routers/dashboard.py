from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.dashboard import (
    DashboardSummary,
    CategoryBreakdownItem,
    MonthlyTrendItem,
)
from app.services.analytics_service import (
    get_dashboard_summary,
    get_category_breakdown,
    get_monthly_trend,
)
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/summary",
    response_model=DashboardSummary
)
def summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_dashboard_summary(db, current_user)


@router.get(
    "/category-breakdown",
    response_model=list[CategoryBreakdownItem]
)
def category_breakdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_category_breakdown(db, current_user)


@router.get(
    "/monthly-trend",
    response_model=list[MonthlyTrendItem]
)
def monthly_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_monthly_trend(db, current_user)
