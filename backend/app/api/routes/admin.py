"""管理员路由 — 审核记录、管理统计"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.database import get_db
from app.models.user import User
from app.services.audit_service import AuditService
from app.services.stats_service import StatsService
from app.utils.response import APIResponse

router = APIRouter()


# ==================== 审核记录 ====================

@router.post("/audit-records", summary="创建审核记录")
def create_audit_record(
    target_type: str = Query(..., description="审核对象类型"),
    target_id: int = Query(..., description="审核对象 ID"),
    action: str = Query(..., pattern="^(approve|reject|flag|review)$"),
    comment: str | None = Query(None),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    record = AuditService.create(db, admin, target_type, target_id, action, comment)
    return APIResponse.created(data={
        "id": record.id,
        "admin_id": record.admin_id,
        "target_type": record.target_type,
        "target_id": record.target_id,
        "action": record.action,
        "comment": record.comment,
        "created_at": record.created_at.isoformat(),
    }, message="审核记录已创建")


@router.get("/audit-records", summary="查看审核记录列表")
def list_audit_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    target_type: str | None = Query(None),
    action: str | None = Query(None, pattern="^(approve|reject|flag|review)$"),
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    items, total = AuditService.list_by_admin(
        db, page=page, page_size=page_size,
        target_type=target_type, action=action,
    )
    return APIResponse.paginated(
        items=[{
            "id": r.id,
            "admin_id": r.admin_id,
            "target_type": r.target_type,
            "target_id": r.target_id,
            "action": r.action,
            "comment": r.comment,
            "created_at": r.created_at.isoformat(),
        } for r in items],
        total=total,
        page=page,
        page_size=page_size,
    )


# ==================== 系统统计 ====================

@router.get("/stats", summary="管理员查看系统整体统计")
def admin_stats(
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    data = StatsService.admin_stats(db)
    return APIResponse.ok(data=data)
