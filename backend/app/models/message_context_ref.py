"""消息上下文引用模型"""

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class MessageContextRef(Base):
    __tablename__ = "message_context_refs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    context_segment_id: Mapped[int] = mapped_column(Integer, ForeignKey("context_segments.id", ondelete="CASCADE"), nullable=False)
    ref_type: Mapped[str] = mapped_column(
        Enum("used", "cited", "generated", name="ref_type"),
        nullable=False, default="used",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    message: Mapped["Message"] = relationship("Message")
    context_segment: Mapped["ContextSegment"] = relationship("ContextSegment", back_populates="message_refs")
