"""反馈 Pydantic 模型"""

from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    feedback_type: str = Field(..., pattern="^(like|dislike|text)$", examples=["like"])
    content: str | None = None
    tags: str | None = Field(None, max_length=255)


class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    message_id: int
    feedback_type: str
    content: str | None
    tags: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
