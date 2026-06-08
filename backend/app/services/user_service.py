"""用户服务 — 个人信息查询与更新"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import AdminUserUpdateRequest, ResetPasswordRequest, UserUpdateRequest


class UserService:

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
        return user

    @staticmethod
    def update_profile(db: Session, user: User, req: UserUpdateRequest) -> User:
        if req.nickname is not None:
            user.nickname = req.nickname
        if req.avatar is not None:
            user.avatar = req.avatar
        if req.phone is not None:
            user.phone = req.phone
        if req.bio is not None:
            user.bio = req.bio
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def admin_update(db: Session, user_id: int, req: AdminUserUpdateRequest) -> User:
        user = UserService.get_by_id(db, user_id)
        if req.nickname is not None:
            user.nickname = req.nickname
        if req.avatar is not None:
            user.avatar = req.avatar
        if req.phone is not None:
            user.phone = req.phone
        if req.bio is not None:
            user.bio = req.bio
        if req.role is not None:
            user.role = req.role
        if req.status is not None:
            user.status = req.status
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def admin_reset_password(db: Session, user_id: int, req: ResetPasswordRequest) -> User:
        user = UserService.get_by_id(db, user_id)
        user.password_hash = hash_password(req.new_password)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def admin_delete(db: Session, user_id: int) -> None:
        user = UserService.get_by_id(db, user_id)
        db.delete(user)
        db.commit()

    @staticmethod
    def list_users(db: Session, page: int = 1, page_size: int = 20, role: str | None = None, status: str | None = None):
        query = db.query(User)
        if role:
            query = query.filter(User.role == role)
        if status:
            query = query.filter(User.status == status)

        total = query.count()
        items = query.order_by(User.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    @staticmethod
    def change_password(db: Session, user: User, old_password: str, new_password: str) -> User:
        if not verify_password(old_password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="原密码错误")
        user.password_hash = hash_password(new_password)
        db.commit()
        db.refresh(user)
        return user
