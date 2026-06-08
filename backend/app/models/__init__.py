"""SQLAlchemy 模型 — 全部导入以确保 Base.metadata 注册"""

from app.models.user import User
from app.models.ai_character import AICharacter
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.message_content import MessageContent
from app.models.message_reasoning import MessageReasoning
from app.models.tool_call import ToolCall
from app.models.tool_result import ToolResult
from app.models.message_metadata import MessageMetadata
from app.models.favorite import MessageFavorite
from app.models.feedback import Feedback
from app.models.system_log import SystemLog
from app.models.audit_record import AuditRecord

__all__ = [
    "User",
    "AICharacter",
    "Conversation",
    "Message",
    "MessageContent",
    "MessageReasoning",
    "ToolCall",
    "ToolResult",
    "MessageMetadata",
    "MessageFavorite",
    "Feedback",
    "SystemLog",
    "AuditRecord",
]
