"""工具调用模型"""

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ToolCall(Base):
    __tablename__ = "tool_calls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    tool_type: Mapped[str] = mapped_column(
        Enum("search", "database", "calculator", "file", "api", "custom", name="tool_type"),
        nullable=False,
        default="custom",
    )
    arguments: Mapped[dict] = mapped_column(JSON, nullable=False)
    call_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("pending", "success", "failed", "timeout", name="tool_call_status"),
        nullable=False,
        default="pending",
    )
    called_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # 关系
    message: Mapped["Message"] = relationship("Message", back_populates="tool_calls")
    result: Mapped["ToolResult | None"] = relationship("ToolResult", back_populates="tool_call", uselist=False)
