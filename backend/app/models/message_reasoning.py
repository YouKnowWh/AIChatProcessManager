"""消息推理过程模型"""

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class MessageReasoning(Base):
    __tablename__ = "message_reasoning"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), unique=True, nullable=False)
    reasoning_content: Mapped[str] = mapped_column(Text, nullable=False)
    visibility: Mapped[str] = mapped_column(
        Enum("hidden", "owner_visible", "admin_visible", "debug_only", name="reasoning_visibility"),
        nullable=False,
        default="hidden",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    # 关系
    message: Mapped["Message"] = relationship("Message", back_populates="reasoning")
