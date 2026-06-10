"""AI 角色 Pydantic 模型"""

from datetime import datetime

from pydantic import BaseModel, Field


class CharacterCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["通用助手"])
    avatar: str | None = Field(None, max_length=500)
    description: str | None = None
    system_prompt: str | None = None
    category: str | None = Field(None, max_length=50)
    tags: str | None = Field(None, max_length=255)
    owner_id: int | None = Field(None, description="角色维护者指定所有者用户 ID")


class CharacterUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    avatar: str | None = Field(None, max_length=500)
    description: str | None = None
    system_prompt: str | None = None
    category: str | None = Field(None, max_length=50)
    tags: str | None = Field(None, max_length=255)
    status: str | None = Field(None, pattern="^(active|disabled)$")


class CharacterResponse(BaseModel):
    id: int
    creator_id: int
    name: str
    avatar: str | None
    description: str | None
    system_prompt: str | None
    category: str | None
    tags: str | None
    status: str
    usage_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CharacterBrief(BaseModel):
    """列表页轻量展示"""
    id: int
    creator_id: int
    name: str
    avatar: str | None
    description: str | None
    category: str | None
    tags: str | None
    status: str
    usage_count: int

    model_config = {"from_attributes": True}
