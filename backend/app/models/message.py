"""消息主表模型"""

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    parent_message_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)
    sender_type: Mapped[str] = mapped_column(
        Enum("user", "ai", "system", "tool", name="sender_type"),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        Enum("user", "assistant", "system", "tool", name="message_role"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        Enum("normal", "hidden", "deleted", name="message_status"),
        nullable=False,
        default="normal",
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    # 关系
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
    parent_message: Mapped["Message | None"] = relationship("Message", remote_side="Message.id", back_populates="child_messages")
    child_messages: Mapped[list["Message"]] = relationship("Message", back_populates="parent_message")
    contents: Mapped[list["MessageContent"]] = relationship("MessageContent", back_populates="message")
    reasoning: Mapped["MessageReasoning | None"] = relationship("MessageReasoning", back_populates="message")
    tool_calls: Mapped[list["ToolCall"]] = relationship("ToolCall", back_populates="message")
    model_metadata: Mapped["MessageMetadata | None"] = relationship("MessageMetadata", back_populates="message")
    feedbacks: Mapped[list["Feedback"]] = relationship("Feedback", back_populates="message")
    favorites: Mapped[list["MessageFavorite"]] = relationship("MessageFavorite", back_populates="message")
