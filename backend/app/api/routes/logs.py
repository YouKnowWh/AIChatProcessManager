"""系统日志路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.database import get_db
from app.models.user import User
from app.services.log_service import LogService
from app.utils.response import APIResponse

router = APIRouter()


@router.get("", summary="管理员查看系统日志")
def list_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: int | None = Query(None),
    action: str | None = Query(None),
    target_type: str | None = Query(None),
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    items, total = LogService.list_by_admin(
        db, page=page, page_size=page_size,
        user_id=user_id, action=action, target_type=target_type,
    )
    return APIResponse.paginated(
        items=[{
            "id": log.id,
            "user_id": log.user_id,
            "username": username or "—",
            "action": log.action,
            "target_type": log.target_type,
            "target_id": log.target_id,
            "detail": log.detail,
            "ip_address": log.ip_address,
            "created_at": log.created_at.isoformat(),
        } for log, username in items],
        total=total,
        page=page,
        page_size=page_size,
    )
