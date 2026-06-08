"""消息 Pydantic 模型"""

from datetime import datetime

from pydantic import BaseModel, Field


class MessageSendRequest(BaseModel):
    content: str = Field(..., min_length=1, examples=["你好，请帮我写一段代码"])


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    parent_message_id: int | None
    sender_type: str
    role: str
    status: str
    sequence_number: int
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageWithContent(MessageResponse):
    contents: list["ContentBlock"] = []


class ContentBlock(BaseModel):
    id: int
    content_type: str
    content: str
    sort_order: int

    model_config = {"from_attributes": True}


class MessageDetail(BaseModel):
    """消息完整详情 — 含所有过程数据"""
    message: MessageResponse
    contents: list[ContentBlock]
    reasoning: "ReasoningBlock | None" = None
    tool_calls: list["ToolCallBlock"] = []
    metadata: "MetadataBlock | None" = None


class ReasoningBlock(BaseModel):
    id: int
    reasoning_content: str
    visibility: str

    model_config = {"from_attributes": True}


class ToolCallBlock(BaseModel):
    id: int
    tool_name: str
    tool_type: str
    arguments: dict
    call_id: str | None
    status: str
    result: "ToolResultBlock | None" = None

    model_config = {"from_attributes": True}


class ToolResultBlock(BaseModel):
    id: int
    result_content: dict
    is_error: bool

    model_config = {"from_attributes": True}


class MetadataBlock(BaseModel):
    id: int
    model_name: str | None
    provider: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    duration_ms: int | None
    finish_reason: str | None
    temperature: float | None
    top_p: float | None

    model_config = {"from_attributes": True}


class MessageSearchRequest(BaseModel):
    keyword: str = Field(..., min_length=1, examples=["Python"])


# 更新前向引用
MessageDetail.model_rebuild()
