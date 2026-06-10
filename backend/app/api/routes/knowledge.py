"""知识库路由"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.knowledge import KnowledgeCreate, KnowledgeResponse, KnowledgeUpdate
from app.services.knowledge_service import KnowledgeService
from app.utils.response import APIResponse

router = APIRouter()


@router.get("/characters/{character_id}/knowledge", summary="查看角色知识库")
def list_knowledge(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = KnowledgeService.list_by_character(db, character_id, current_user)
    return APIResponse.ok(data=[KnowledgeResponse.model_validate(e).model_dump() for e in items])


@router.post("/characters/{character_id}/knowledge", summary="添加知识条目")
def create_knowledge(
    character_id: int,
    req: KnowledgeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = KnowledgeService.create(db, character_id, current_user, req)
    return APIResponse.created(data=KnowledgeResponse.model_validate(entry).model_dump(), message="知识条目已添加")


@router.put("/knowledge/{entry_id}", summary="更新知识条目")
def update_knowledge(
    entry_id: int,
    req: KnowledgeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = KnowledgeService.update(db, entry_id, current_user, req)
    return APIResponse.ok(data=KnowledgeResponse.model_validate(entry).model_dump(), message="已更新")


@router.delete("/knowledge/{entry_id}", summary="删除知识条目")
def delete_knowledge(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    KnowledgeService.delete(db, entry_id, current_user)
    return APIResponse.ok(message="已删除")
