"""知识库服务"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ai_character import AICharacter
from app.models.knowledge_entry import KnowledgeEntry
from app.models.user import User
from app.schemas.knowledge import KnowledgeCreate, KnowledgeUpdate


class KnowledgeService:

    @staticmethod
    def list_by_character(db: Session, character_id: int, user: User):
        """查看角色的知识库"""
        character = db.query(AICharacter).filter(AICharacter.id == character_id).first()
        if not character:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI 角色不存在")
        if user.role != "admin" and character.creator_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权访问")

        return db.query(KnowledgeEntry).filter(
            KnowledgeEntry.character_id == character_id,
            KnowledgeEntry.status == "active",
        ).order_by(KnowledgeEntry.id.desc()).all()

    @staticmethod
    def create(db: Session, character_id: int, user: User, req: KnowledgeCreate) -> KnowledgeEntry:
        character = db.query(AICharacter).filter(AICharacter.id == character_id).first()
        if not character:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI 角色不存在")
        if user.role != "admin" and character.creator_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权操作")

        entry = KnowledgeEntry(
            character_id=character_id,
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

        character = entry.character
        if user.role != "admin" and character.creator_id != user.id:
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
        if user.role != "admin" and entry.character.creator_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权操作")
        db.delete(entry)
        db.commit()
