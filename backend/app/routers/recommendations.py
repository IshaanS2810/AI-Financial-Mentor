from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.recommendation import PersonalizedRecommendationsResponse
from app.services.recommendation_service import generate_personalized_recommendations
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/recommendations",
    tags=["Personalized Recommendations"]
)


@router.get(
    "",
    response_model=PersonalizedRecommendationsResponse
)
def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generates personalized, rule-based educational investment recommendations for the authenticated user."""
    return generate_personalized_recommendations(db, current_user)
