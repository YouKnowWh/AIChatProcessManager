"""工具结果模型"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ToolResult(Base):
    __tablename__ = "tool_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tool_call_id: Mapped[int] = mapped_column(Integer, ForeignKey("tool_calls.id", ondelete="CASCADE"), unique=True, nullable=False)
    result_content: Mapped[dict] = mapped_column(JSON, nullable=False)
    is_error: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    # 关系
    tool_call: Mapped["ToolCall"] = relationship("ToolCall", back_populates="result")
