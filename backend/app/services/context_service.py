"""上下文服务 — 构建和查询对话上下文片段"""

import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.context_segment import ContextSegment
from app.models.message import Message
from app.models.message_content import MessageContent
from app.models.message_context_ref import MessageContextRef
from app.models.conversation import Conversation
from app.models.user import User


class ContextService:

    @staticmethod
    def build_recent_context(db: Session, conversation_id: int, user_id: int,
                             ai_message_id: int, max_messages: int = 5) -> ContextSegment | None:
        """基于最近 N 条正常消息构建上下文片段"""
        recent = (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation_id,
                Message.status == "normal",
            )
            .order_by(Message.sequence_number.desc())
            .limit(max_messages)
            .all()
        )
        if len(recent) < 2:
            return None

        recent.reverse()
        # 构建摘要
        lines = []
        total_chars = 0
        for msg in recent:
            contents = db.query(MessageContent).filter(
                MessageContent.message_id == msg.id
            ).order_by(MessageContent.sort_order).all()
            text = " ".join(c.content for c in contents)
            prefix = "user" if msg.sender_type == "user" else "assistant"
            lines.append(f"{prefix}: {text[:300]}")
            total_chars += len(text)

        summary = "\n".join(lines)
        token_est = int(total_chars / 2.5)  # rough token estimate

        segment = ContextSegment(
            conversation_id=conversation_id,
            segment_type="recent_messages",
            summary_text=summary,
            start_message_id=recent[0].id,
            end_message_id=recent[-1].id,
            token_count=token_est,
            status="active",
        )
        db.add(segment)
        db.flush()
        return segment

    @staticmethod
    def link_message_context(db: Session, message_id: int, segment_id: int,
                             ref_type: str = "used") -> MessageContextRef:
        """建立消息与上下文片段的引用关系"""
        ref = MessageContextRef(
            message_id=message_id,
            context_segment_id=segment_id,
            ref_type=ref_type,
        )
        db.add(ref)
        return ref

    @staticmethod
    def get_conversation_contexts(db: Session, conversation_id: int, user: User):
        """查询会话的活跃上下文片段"""
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="会话不存在")
        if conv.user_id != user.id and user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权访问")

        return db.query(ContextSegment).filter(
            ContextSegment.conversation_id == conversation_id,
            ContextSegment.status == "active",
        ).order_by(ContextSegment.created_at.desc()).all()

    @staticmethod
    def get_message_contexts(db: Session, message_id: int, user: User):
        """查询某条消息引用的上下文片段"""
        msg = db.query(Message).filter(Message.id == message_id).first()
        if not msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="消息不存在")
        conv = msg.conversation
        if conv.user_id != user.id and user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权访问")

        refs = db.query(MessageContextRef).filter(
            MessageContextRef.message_id == message_id,
        ).all()

        segment_ids = [r.context_segment_id for r in refs]
        segments = db.query(ContextSegment).filter(
            ContextSegment.id.in_(segment_ids)
        ).all() if segment_ids else []

        return segments
