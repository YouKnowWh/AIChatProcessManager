"""反馈服务"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.feedback import Feedback
from app.models.message import Message
from app.models.user import User
from app.schemas.feedback import FeedbackCreate


class FeedbackService:

    @staticmethod
    def create(db: Session, user: User, message_id: int, req: FeedbackCreate) -> Feedback:
        """提交反馈"""
        msg = db.query(Message).filter(Message.id == message_id).first()
        if not msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="消息不存在")
        if msg.conversation.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权反馈该消息")

        # 同用户对同一消息同类型不重复（like/dislike 不可重复，text 可以多条）
        if req.feedback_type in ("like", "dislike"):
            existing = db.query(Feedback).filter(
                Feedback.user_id == user.id,
                Feedback.message_id == message_id,
                Feedback.feedback_type == req.feedback_type,
            ).first()
            if existing:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"已经{'点赞' if req.feedback_type == 'like' else '点踩'}过该消息")

            # 不能同时点赞又点踩（允许切换：删除旧记录再创建新的）
            opposite = "dislike" if req.feedback_type == "like" else "like"
            opposite_record = db.query(Feedback).filter(
                Feedback.user_id == user.id,
                Feedback.message_id == message_id,
                Feedback.feedback_type == opposite,
            ).first()
            if opposite_record:
                db.delete(opposite_record)

        character_id = msg.conversation.character_id
        feedback = Feedback(
            user_id=user.id,
            message_id=message_id,
            character_id=character_id,
            feedback_type=req.feedback_type,
            content=req.content,
            tags=req.tags,
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        return feedback

    @staticmethod
    def list_by_user(db: Session, user: User, page: int = 1, page_size: int = 20):
        """查看自己的反馈"""
        query = db.query(Feedback).filter(Feedback.user_id == user.id)
        total = query.count()
        items = query.order_by(Feedback.created_at.desc()).offset(
            (page - 1) * page_size
        ).limit(page_size).all()
        return items, total

    @staticmethod
    def list_by_admin(db: Session, page: int = 1, page_size: int = 20,
                      feedback_type: str | None = None, character_id: int | None = None):
        """管理员查看所有反馈"""
        query = db.query(Feedback)
        if feedback_type:
            query = query.filter(Feedback.feedback_type == feedback_type)
        if character_id:
            query = query.filter(Feedback.character_id == character_id)
        total = query.count()
        items = query.order_by(Feedback.created_at.desc()).offset(
            (page - 1) * page_size
        ).limit(page_size).all()
        return items, total
