from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import (
    chat_with_mentor,
    get_user_chat_history,
    delete_chat_history_item,
)
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/ai",
    tags=["AI Financial Mentor"]
)


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED
)
def send_chat_message(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return chat_with_mentor(payload.message, db, current_user)


@router.get(
    "/history",
    response_model=list[ChatResponse]
)
def get_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_chat_history(db, current_user)


@router.delete(
    "/history/{chat_id}"
)
def delete_history_item(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_chat_history_item(chat_id, db, current_user)
