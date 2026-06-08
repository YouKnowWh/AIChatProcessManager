"""认证路由 — 注册 / 登录 / 当前用户 / 登出"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserBrief
from app.services.auth_service import AuthService
from app.utils.response import APIResponse

router = APIRouter()


@router.post("/register", response_model=dict, summary="用户注册")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    result = AuthService.register(db, req)
    return APIResponse.created(
        data=result.model_dump(),
        message="注册成功",
    )


@router.post("/login", response_model=dict, summary="用户登录")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    result = AuthService.login(db, req)
    # 更新最后登录时间
    user = db.query(User).filter(User.id == result.user.id).first()
    if user:
        from datetime import datetime
        user.last_login_at = datetime.now()
        db.commit()
    return APIResponse.ok(
        data=result.model_dump(),
        message="登录成功",
    )


@router.get("/me", response_model=dict, summary="获取当前用户信息")
def me(current_user: User = Depends(get_current_user)):
    return APIResponse.ok(data=UserBrief.model_validate(current_user).model_dump())


@router.post("/logout", response_model=dict, summary="用户登出")
def logout(current_user: User = Depends(get_current_user)):
    # JWT 无状态，客户端丢弃 token 即可
    return APIResponse.ok(message="已登出")
