"""知识库服务（用户级别）"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.knowledge_entry import KnowledgeEntry
from app.models.user import User
from app.schemas.knowledge import KnowledgeCreate, KnowledgeUpdate


class KnowledgeService:

    @staticmethod
    def list_by_user(db: Session, user: User):
        return db.query(KnowledgeEntry).filter(
            KnowledgeEntry.user_id == user.id,
            KnowledgeEntry.status == "active",
        ).order_by(KnowledgeEntry.id.desc()).all()

    @staticmethod
    def create(db: Session, user: User, req: KnowledgeCreate) -> KnowledgeEntry:
        entry = KnowledgeEntry(
            user_id=user.id,
            title=req.title,
            content=req.content,
            content_type=req.content_type,
            source=req.source,
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def update(db: Session, entry_id: int, user: User, req: KnowledgeUpdate) -> KnowledgeEntry:
        entry = db.query(KnowledgeEntry).filter(KnowledgeEntry.id == entry_id).first()
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="知识条目不存在")
        if user.role != "admin" and entry.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权操作")

        if req.title is not None: entry.title = req.title
        if req.content is not None: entry.content = req.content
        if req.content_type is not None: entry.content_type = req.content_type
        if req.source is not None: entry.source = req.source
        if req.status is not None: entry.status = req.status
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def delete(db: Session, entry_id: int, user: User) -> None:
        entry = db.query(KnowledgeEntry).filter(KnowledgeEntry.id == entry_id).first()
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="知识条目不存在")
        if user.role != "admin" and entry.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权操作")
        db.delete(entry)
        db.commit()

    @staticmethod
    def admin_stats(db: Session) -> list[dict]:
        """管理员查看各用户知识库概况（只统计，不暴露内容）"""
        from sqlalchemy import func
        rows = db.query(
            KnowledgeEntry.user_id, User.username,
            func.count(KnowledgeEntry.id).label("total"),
            func.sum(func.if_(KnowledgeEntry.status == "active", 1, 0)).label("active"),
        ).join(User, User.id == KnowledgeEntry.user_id).group_by(
            KnowledgeEntry.user_id, User.username
        ).all()
        return [
            {"user_id": r[0], "username": r[1], "total_entries": r[2], "active_entries": r[3] or 0}
            for r in rows
        ]
