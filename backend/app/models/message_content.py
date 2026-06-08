"""消息正文模型"""

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class MessageContent(Base):
    __tablename__ = "message_contents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    content_type: Mapped[str] = mapped_column(
        Enum("text", "markdown", "code", "link", "image", name="content_type"),
        nullable=False,
        default="text",
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    # 关系
    message: Mapped["Message"] = relationship("Message", back_populates="contents")
