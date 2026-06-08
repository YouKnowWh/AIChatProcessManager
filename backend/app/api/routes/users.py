"""用户路由 — 个人信息查看与修改"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import AdminUserUpdateRequest, ResetPasswordRequest, UserUpdateRequest, UserResponse
from app.services.user_service import UserService
from app.utils.response import APIResponse

router = APIRouter()


# ==================== 当前用户 ====================

@router.get("/users/me", summary="查看个人信息")
def get_me(current_user: User = Depends(get_current_user)):
    return APIResponse.ok(data=UserResponse.model_validate(current_user).model_dump())


@router.put("/users/me", summary="修改个人信息")
def update_me(
    req: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = UserService.update_profile(db, current_user, req)
    return APIResponse.ok(data=UserResponse.model_validate(user).model_dump(), message="更新成功")


# ==================== 管理员用户管理 ====================

@router.get("/admin/users", summary="管理员查看用户列表")
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    items, total = UserService.list_users(db, page=page, page_size=page_size, role=role, status=status)
    return APIResponse.paginated(
        items=[UserResponse.model_validate(u).model_dump() for u in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/admin/users/{user_id}", summary="管理员查看用户详情")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    user = UserService.get_by_id(db, user_id)
    return APIResponse.ok(data=UserResponse.model_validate(user).model_dump())


@router.put("/admin/users/{user_id}", summary="管理员修改用户")
def admin_update_user(
    user_id: int,
    req: AdminUserUpdateRequest,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    user = UserService.admin_update(db, user_id, req)
    return APIResponse.ok(data=UserResponse.model_validate(user).model_dump(), message="更新成功")


@router.put("/admin/users/{user_id}/password", summary="管理员重置用户密码")
def admin_reset_password(
    user_id: int,
    req: ResetPasswordRequest,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    UserService.admin_reset_password(db, user_id, req)
    return APIResponse.ok(message="密码已重置")


@router.put("/admin/users/{user_id}/disable", summary="管理员禁用用户")
def disable_user(
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    user = UserService.admin_update(db, user_id, AdminUserUpdateRequest(status="disabled"))
    return APIResponse.ok(data=UserResponse.model_validate(user).model_dump(), message="用户已禁用")


@router.put("/admin/users/{user_id}/enable", summary="管理员启用用户")
def enable_user(
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    user = UserService.admin_update(db, user_id, AdminUserUpdateRequest(status="active"))
    return APIResponse.ok(data=UserResponse.model_validate(user).model_dump(), message="用户已启用")


@router.delete("/admin/users/{user_id}", summary="管理员删除用户")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    UserService.admin_delete(db, user_id)
    return APIResponse.ok(message="用户已删除")
