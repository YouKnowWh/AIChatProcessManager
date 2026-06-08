"""会话 Pydantic 模型"""

from datetime import datetime

from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    character_id: int = Field(..., examples=[1])
    title: str | None = Field(None, max_length=200, examples=["随便聊聊"])


class ConversationUpdate(BaseModel):
    title: str | None = Field(None, max_length=200)


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    character_id: int
    title: str | None
    status: str
    last_message_at: datetime | None
    message_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConversationBrief(BaseModel):
    """侧边栏展示用"""
    id: int
    character_id: int
    character_name: str | None = None
    character_avatar: str | None = None
    title: str | None
    status: str
    last_message_at: datetime | None
    message_count: int = 0

    model_config = {"from_attributes": True}
