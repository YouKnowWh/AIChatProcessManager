"""收藏路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.services.favorite_service import FavoriteService
from app.utils.response import APIResponse

router = APIRouter()


@router.post("/messages/{message_id}/favorite", summary="收藏消息（切换）")
def toggle_favorite(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = FavoriteService.toggle_favorite(db, current_user, message_id)
    return APIResponse.ok(data=result)


@router.delete("/messages/{message_id}/favorite", summary="取消收藏")
def remove_favorite(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    FavoriteService.remove_favorite(db, current_user, message_id)
    return APIResponse.ok(message="已取消收藏")


@router.get("", summary="查看我的收藏列表")
def list_favorites(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = FavoriteService.list_by_user(db, current_user, page=page, page_size=page_size)
    return APIResponse.paginated(items=items, total=total, page=page, page_size=page_size)
