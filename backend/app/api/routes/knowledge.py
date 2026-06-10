"""知识库路由（用户级别）"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.knowledge import KnowledgeCreate, KnowledgeResponse, KnowledgeUpdate
from app.services.knowledge_service import KnowledgeService
from app.utils.response import APIResponse

router = APIRouter()


@router.get("/knowledge", summary="查看我的知识库")
def list_knowledge(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = KnowledgeService.list_by_user(db, current_user)
    return APIResponse.ok(data=[KnowledgeResponse.model_validate(e).model_dump() for e in items])


@router.post("/knowledge", summary="添加知识条目")
def create_knowledge(
    req: KnowledgeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = KnowledgeService.create(db, current_user, req)
    return APIResponse.created(data=KnowledgeResponse.model_validate(entry).model_dump(), message="已添加")


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


# 管理员查看知识库概况
@router.get("/admin/knowledge-stats", summary="管理员查看知识库概况")
def admin_knowledge_stats(
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    stats = KnowledgeService.admin_stats(db)
    return APIResponse.ok(data=stats)
