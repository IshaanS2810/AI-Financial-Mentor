from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000, description="User's question or financial query")


class ChatResponse(BaseModel):
    id: int
    user_id: int
    user_message: str
    ai_response: str
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
