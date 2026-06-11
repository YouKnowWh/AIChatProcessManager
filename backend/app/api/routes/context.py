"""上下文路由"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.context import ContextSegmentResponse
from app.services.context_service import ContextService
from app.utils.response import APIResponse

router = APIRouter()


@router.get("/conversations/{conversation_id}/contexts", summary="查看会话上下文片段")
def get_conversation_contexts(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    segments = ContextService.get_conversation_contexts(db, conversation_id, current_user)
    return APIResponse.ok(data=[ContextSegmentResponse.model_validate(s).model_dump() for s in segments])


@router.get("/messages/{message_id}/contexts", summary="查看消息引用的上下文")
def get_message_contexts(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    segments = ContextService.get_message_contexts(db, message_id, current_user)
    return APIResponse.ok(data=[ContextSegmentResponse.model_validate(s).model_dump() for s in segments])
