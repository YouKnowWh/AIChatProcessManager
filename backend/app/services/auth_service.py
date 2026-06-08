"""认证服务 — 注册、登录、JWT 签发"""

from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserBrief


class AuthService:

    @staticmethod
    def register(db: Session, req: RegisterRequest) -> TokenResponse:
        # 检查用户名是否已存在
        if db.query(User).filter(User.username == req.username).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="用户名已存在")

        # 检查邮箱是否已存在
        if db.query(User).filter(User.email == req.email).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="邮箱已存在")

        # 创建用户
        user = User(
            username=req.username,
            email=req.email,
            password_hash=hash_password(req.password),
            nickname=req.nickname or req.username,
            role="user",
            status="active",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        return AuthService._build_token(user)

    @staticmethod
    def login(db: Session, req: LoginRequest) -> TokenResponse:
        user = db.query(User).filter(User.username == req.username).first()

        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

        if user.status == "disabled":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="账户已被禁用")

        return AuthService._build_token(user)

    @staticmethod
    def _build_token(user: User) -> TokenResponse:
        expires_delta = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        token = create_access_token(data={"sub": user.id}, expires_delta=expires_delta)

        return TokenResponse(
            access_token=token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRE_MINUTES * 60,
            user=UserBrief(
                id=user.id,
                username=user.username,
                email=user.email,
                nickname=user.nickname,
                role=user.role,
                avatar=user.avatar,
            ),
        )
