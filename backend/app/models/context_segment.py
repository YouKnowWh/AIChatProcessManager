"""上下文片段模型"""

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ContextSegment(Base):
    __tablename__ = "context_segments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    segment_type: Mapped[str] = mapped_column(
        Enum("recent_messages", "manual", "system", name="segment_type"),
        nullable=False, default="recent_messages",
    )
    summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_message_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)
    end_message_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)
    token_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(
        Enum("active", "archived", name="context_status"),
        nullable=False, default="active",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    conversation: Mapped["Conversation"] = relationship("Conversation")
    message_refs: Mapped[list["MessageContextRef"]] = relationship("MessageContextRef", back_populates="context_segment")
