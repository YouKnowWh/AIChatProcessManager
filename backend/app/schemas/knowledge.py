"""知识库 Pydantic 模型"""

from datetime import datetime

from pydantic import BaseModel, Field


class KnowledgeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    content_type: str = Field(default="text", pattern="^(text|markdown|file)$")
    source: str | None = Field(None, max_length=500)


class KnowledgeUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = None
    content_type: str | None = Field(None, pattern="^(text|markdown|file)$")
    source: str | None = Field(None, max_length=500)
    status: str | None = Field(None, pattern="^(active|disabled)$")


class KnowledgeResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    content_type: str
    source: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
