"""AI 角色服务"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ai_character import AICharacter
from app.models.user import User
from app.schemas.ai_character import CharacterCreate, CharacterUpdate


class CharacterService:

    @staticmethod
    def list_active(db: Session, category: str | None = None, search: str | None = None) -> list[AICharacter]:
        """列出所有已启用的角色"""
        query = db.query(AICharacter).filter(AICharacter.status == "active")
        if category:
            query = query.filter(AICharacter.category == category)
        if search:
            query = query.filter(AICharacter.name.contains(search))
        return query.order_by(AICharacter.usage_count.desc()).all()

    @staticmethod
    def list_by_creator(db: Session, creator: User, page: int = 1, page_size: int = 20):
        """角色维护者查看自己创建的角色"""
        query = db.query(AICharacter).filter(AICharacter.creator_id == creator.id)
        total = query.count()
        items = query.order_by(AICharacter.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    @staticmethod
    def list_all(db: Session, page: int = 1, page_size: int = 20, status: str | None = None, category: str | None = None):
        """管理员查看所有角色"""
        query = db.query(AICharacter)
        if status:
            query = query.filter(AICharacter.status == status)
        if category:
            query = query.filter(AICharacter.category == category)
        total = query.count()
        items = query.order_by(AICharacter.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    @staticmethod
    def get_by_id(db: Session, character_id: int) -> AICharacter:
        character = db.query(AICharacter).filter(AICharacter.id == character_id).first()
        if not character:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI 角色不存在")
        return character

    @staticmethod
    def create(db: Session, creator: User, req: CharacterCreate) -> AICharacter:
        if db.query(AICharacter).filter(AICharacter.name == req.name).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="角色名称已存在")

        character = AICharacter(
            creator_id=creator.id,
            name=req.name,
            avatar=req.avatar,
            description=req.description,
            system_prompt=req.system_prompt,
            category=req.category,
            tags=req.tags,
            status="active",
        )
        db.add(character)
        db.commit()
        db.refresh(character)
        return character

    @staticmethod
    def update(db: Session, character: AICharacter, req: CharacterUpdate) -> AICharacter:
        if req.name is not None and req.name != character.name:
            if db.query(AICharacter).filter(AICharacter.name == req.name, AICharacter.id != character.id).first():
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="角色名称已存在")
            character.name = req.name
        if req.avatar is not None:
            character.avatar = req.avatar
        if req.description is not None:
            character.description = req.description
        if req.system_prompt is not None:
            character.system_prompt = req.system_prompt
        if req.category is not None:
            character.category = req.category
        if req.tags is not None:
            character.tags = req.tags
        if req.status is not None:
            # 只有管理员可以改状态，角色维护者只能编辑基本信息
            character.status = req.status
        db.commit()
        db.refresh(character)
        return character

    @staticmethod
    def delete(db: Session, character: AICharacter) -> None:
        db.delete(character)
        db.commit()

    @staticmethod
    def disable(db: Session, character: AICharacter) -> AICharacter:
        character.status = "disabled"
        db.commit()
        db.refresh(character)
        return character

    @staticmethod
    def increment_usage(db: Session, character: AICharacter) -> None:
        """增加角色使用次数"""
        character.usage_count += 1
        db.commit()
