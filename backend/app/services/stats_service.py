"""统计服务"""

from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.favorite import MessageFavorite
from app.models.feedback import Feedback
from app.models.message import Message
from app.models.user import User


class StatsService:

    @staticmethod
    def personal_stats(db: Session, user: User) -> dict:
        conv_count = db.query(Conversation).filter(
            Conversation.user_id == user.id, Conversation.status != "deleted",
        ).count()
        msg_count = db.query(Message).join(Conversation).filter(
            Conversation.user_id == user.id, Message.status == "normal",
        ).count()
        fav_count = db.query(MessageFavorite).filter(MessageFavorite.user_id == user.id).count()
        fb_count = db.query(Feedback).filter(Feedback.user_id == user.id).count()

        return {
            "user_id": user.id, "username": user.username,
            "conversation_count": conv_count, "message_count": msg_count,
            "favorite_count": fav_count, "feedback_count": fb_count,
        }

    @staticmethod
    def admin_stats(db: Session) -> dict:
        total_users = db.query(User).filter(User.status == "active").count()
        total_disabled_users = db.query(User).filter(User.status == "disabled").count()
        total_conversations = db.query(Conversation).filter(Conversation.status != "deleted").count()
        archived_conversations = db.query(Conversation).filter(Conversation.status == "archived").count()
        total_messages = db.query(Message).filter(Message.status == "normal").count()
        hidden_messages = db.query(Message).filter(Message.status == "hidden").count()
        total_favorites = db.query(MessageFavorite).count()
        total_likes = db.query(Feedback).filter(Feedback.feedback_type == "like").count()
        total_dislikes = db.query(Feedback).filter(Feedback.feedback_type == "dislike").count()
        total_text_feedbacks = db.query(Feedback).filter(Feedback.feedback_type == "text").count()

        from sqlalchemy import func
        top_users = (
            db.query(User.username, func.count(Message.id).label("cnt"))
            .join(Conversation, Conversation.user_id == User.id)
            .join(Message, Message.conversation_id == Conversation.id)
            .filter(Message.status == "normal")
            .group_by(User.id).order_by(func.count(Message.id).desc()).limit(5).all()
        )

        return {
            "users": {"total_active": total_users, "total_disabled": total_disabled_users},
            "conversations": {"total_active": total_conversations - archived_conversations, "archived": archived_conversations},
            "messages": {"total_normal": total_messages, "hidden": hidden_messages},
            "interactions": {
                "total_favorites": total_favorites, "total_likes": total_likes,
                "total_dislikes": total_dislikes, "total_text_feedbacks": total_text_feedbacks,
            },
            "top_users": [{"username": u[0], "message_count": u[1]} for u in top_users],
        }
