"""收藏服务"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.favorite import MessageFavorite
from app.models.message import Message
from app.models.user import User


class FavoriteService:

    @staticmethod
    def toggle_favorite(db: Session, user: User, message_id: int) -> dict:
        """收藏/取消收藏切换"""
        # 校验消息存在
        msg = db.query(Message).filter(Message.id == message_id).first()
        if not msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="消息不存在")

        existing = db.query(MessageFavorite).filter(
            MessageFavorite.user_id == user.id,
            MessageFavorite.message_id == message_id,
        ).first()

        if existing:
            db.delete(existing)
            db.commit()
            return {"favorited": False, "message": "已取消收藏"}
        else:
            favorite = MessageFavorite(user_id=user.id, message_id=message_id)
            db.add(favorite)
            db.commit()
            return {"favorited": True, "message": "已收藏"}

    @staticmethod
    def list_by_user(db: Session, user: User, page: int = 1, page_size: int = 20):
        """查看收藏列表"""
        query = db.query(MessageFavorite).filter(MessageFavorite.user_id == user.id)
        total = query.count()
        favorites = (
            query
            .order_by(MessageFavorite.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        items = []
        for fav in favorites:
            msg = fav.message
            # 取第一条 content 作为预览
            preview = ""
            if msg and msg.contents:
                first = sorted(msg.contents, key=lambda x: x.sort_order)[0]
                preview = first.content[:100]

            items.append({
                "id": fav.id,
                "user_id": fav.user_id,
                "message_id": fav.message_id,
                "created_at": fav.created_at.isoformat(),
                "message_preview": preview,
                "conversation_id": msg.conversation_id if msg else None,
                "conversation_title": msg.conversation.title if msg and msg.conversation else None,
                "sender_type": msg.sender_type if msg else None,
            })

        return items, total

    @staticmethod
    def remove_favorite(db: Session, user: User, message_id: int) -> None:
        """取消收藏（DELETE 方式）"""
        fav = db.query(MessageFavorite).filter(
            MessageFavorite.user_id == user.id,
            MessageFavorite.message_id == message_id,
        ).first()
        if not fav:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未收藏该消息")
        db.delete(fav)
        db.commit()

    @staticmethod
    def is_favorited(db: Session, user: User, message_id: int) -> bool:
        """检查是否已收藏"""
        return db.query(MessageFavorite).filter(
            MessageFavorite.user_id == user.id,
            MessageFavorite.message_id == message_id,
        ).first() is not None
