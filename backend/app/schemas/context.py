"""上下文 Pydantic 模型"""

from datetime import datetime

from pydantic import BaseModel


class ContextSegmentResponse(BaseModel):
    id: int
    conversation_id: int
    segment_type: str
    summary_text: str | None
    start_message_id: int | None
    end_message_id: int | None
    token_count: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageContextRefResponse(BaseModel):
    id: int
    message_id: int
    context_segment_id: int
    ref_type: str
    created_at: datetime

    model_config = {"from_attributes": True}
