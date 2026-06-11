"""会话 Pydantic 模型"""

from datetime import datetime

from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    title: str | None = Field(None, max_length=200, examples=["新的聊天"])


class ConversationUpdate(BaseModel):
    title: str | None = Field(None, max_length=200)


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: str | None
    status: str
    last_message_at: datetime | None
    message_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
