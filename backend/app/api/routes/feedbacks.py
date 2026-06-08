"""反馈路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.services.feedback_service import FeedbackService
from app.utils.response import APIResponse

router = APIRouter()


@router.post("/messages/{message_id}/feedback", summary="提交反馈")
def create_feedback(
    message_id: int,
    req: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    feedback = FeedbackService.create(db, current_user, message_id, req)
    return APIResponse.created(
        data=FeedbackResponse.model_validate(feedback).model_dump(),
        message="反馈提交成功",
    )


@router.get("", summary="查看我的反馈")
def list_my_feedbacks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = FeedbackService.list_by_user(db, current_user, page=page, page_size=page_size)
    return APIResponse.paginated(
        items=[FeedbackResponse.model_validate(f).model_dump() for f in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/admin/feedbacks", summary="管理员查看所有反馈")
def admin_list_feedbacks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    feedback_type: str | None = Query(None, pattern="^(like|dislike|text)$"),
    character_id: int | None = Query(None),
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    items, total = FeedbackService.list_by_admin(
        db, page=page, page_size=page_size,
        feedback_type=feedback_type, character_id=character_id,
    )
    return APIResponse.paginated(
        items=[FeedbackResponse.model_validate(f).model_dump() for f in items],
        total=total,
        page=page,
        page_size=page_size,
    )
