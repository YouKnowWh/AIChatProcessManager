"""统计路由"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_user
from app.db.database import get_db
from app.models.user import User
from app.services.stats_service import StatsService
from app.utils.response import APIResponse

router = APIRouter()


@router.get("/me", summary="查看个人统计数据")
def personal_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = StatsService.personal_stats(db, current_user)
    return APIResponse.ok(data=data)


# 管理员统计在 admin 路由中: GET /api/admin/stats
