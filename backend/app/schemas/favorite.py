"""收藏 Pydantic 模型"""

from datetime import datetime

from pydantic import BaseModel


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    message_id: int
    created_at: datetime
    message_preview: str | None = None
    conversation_id: int | None = None
    conversation_title: str | None = None

    model_config = {"from_attributes": True}
