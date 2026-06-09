"""会话服务"""

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ai_character import AICharacter
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User
from app.schemas.conversation import ConversationCreate, ConversationUpdate


class ConversationService:

    @staticmethod
    def list_by_user(db: Session, user: User, status: str | None = None, character_id: int | None = None):
        """列出当前用户的会话"""
        query = db.query(Conversation).filter(
            Conversation.user_id == user.id,
            Conversation.status != "deleted",
        )
        if status:
            query = query.filter(Conversation.status == status)
        if character_id:
            query = query.filter(Conversation.character_id == character_id)

        items = query.order_by(
            Conversation.last_message_at.is_(None).desc(),  # NULL 排最前（新会话）
            Conversation.last_message_at.desc(),
            Conversation.id.desc(),
        ).all()

        # 附带消息数量
        results = []
        for conv in items:
            msg_count = db.query(Message).filter(Message.conversation_id == conv.id).count()
            results.append({
                "id": conv.id,
                "user_id": conv.user_id,
                "character_id": conv.character_id,
                "character_name": conv.character.name if conv.character else None,
                "character_avatar": conv.character.avatar if conv.character else None,
                "title": conv.title,
                "status": conv.status,
                "last_message_at": conv.last_message_at,
                "message_count": msg_count,
                "created_at": conv.created_at,
                "updated_at": conv.updated_at,
            })
        return results

    @staticmethod
    def get_by_id(db: Session, conversation_id: int, user: User | None = None) -> Conversation:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="会话不存在")
        if user and conversation.user_id != user.id and user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权访问该会话")
        return conversation

    @staticmethod
    def create(db: Session, user: User, req: ConversationCreate) -> Conversation:
        # 验证角色存在且可用
        character = db.query(AICharacter).filter(
            AICharacter.id == req.character_id,
            AICharacter.status == "active",
        ).first()
        if not character:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="AI 角色不存在或已禁用")

        conversation = Conversation(
            user_id=user.id,
            character_id=req.character_id,
            title=req.title or f"与 {character.name} 的对话",
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def update(db: Session, conversation: Conversation, req: ConversationUpdate) -> Conversation:
        if req.title is not None:
            conversation.title = req.title
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def archive(db: Session, conversation: Conversation) -> Conversation:
        conversation.status = "archived"
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def unarchive(db: Session, conversation: Conversation) -> Conversation:
        conversation.status = "active"
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def soft_delete(db: Session, conversation: Conversation) -> Conversation:
        conversation.status = "deleted"
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def touch_last_message(db: Session, conversation: Conversation) -> None:
        """更新最后消息时间"""
        conversation.last_message_at = datetime.now()
        db.commit()
