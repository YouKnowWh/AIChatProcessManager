"""会话路由"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.conversation import ConversationCreate, ConversationResponse, ConversationUpdate
from app.services.conversation_service import ConversationService
from app.utils.response import APIResponse

router = APIRouter()


@router.get("", summary="查看我的会话列表")
def list_conversations(
    status: str | None = Query(None, pattern="^(active|archived)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = ConversationService.list_by_user(
        db, current_user, status=status,
    )
    return APIResponse.ok(data=items)


@router.post("", summary="创建新会话")
def create_conversation(
    req: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="管理员不允许创建会话")
    conversation = ConversationService.create(db, current_user, req)
    return APIResponse.created(
        data=ConversationResponse.model_validate(conversation).model_dump(),
        message="会话创建成功",
    )


@router.get("/{conversation_id}", summary="查看会话详情")
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = ConversationService.get_by_id(db, conversation_id, current_user)
    return APIResponse.ok(data=ConversationResponse.model_validate(conversation).model_dump())


@router.put("/{conversation_id}", summary="更新会话（重命名）")
def update_conversation(
    conversation_id: int,
    req: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = ConversationService.get_by_id(db, conversation_id, current_user)
    conversation = ConversationService.update(db, conversation, req)
    return APIResponse.ok(
        data=ConversationResponse.model_validate(conversation).model_dump(),
        message="更新成功",
    )


@router.put("/{conversation_id}/archive", summary="归档会话")
def archive_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = ConversationService.get_by_id(db, conversation_id, current_user)
    conversation = ConversationService.archive(db, conversation)
    return APIResponse.ok(
        data=ConversationResponse.model_validate(conversation).model_dump(),
        message="会话已归档",
    )


@router.put("/{conversation_id}/unarchive", summary="取消归档")
def unarchive_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = ConversationService.get_by_id(db, conversation_id, current_user)
    conversation = ConversationService.unarchive(db, conversation)
    return APIResponse.ok(
        data=ConversationResponse.model_validate(conversation).model_dump(),
        message="会话已恢复",
    )


@router.delete("/{conversation_id}", summary="删除会话（软删除）")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = ConversationService.get_by_id(db, conversation_id, current_user)
    conversation = ConversationService.soft_delete(db, conversation)
    return APIResponse.ok(message="会话已删除")
