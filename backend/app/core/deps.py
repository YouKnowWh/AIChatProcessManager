"""依赖注入 — JWT 鉴权与角色权限校验"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User

security_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    """从 JWT 中解析当前用户，注入到路由"""
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的认证令牌")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌缺少用户标识")
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌用户标识无效")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在")

    if user.status == "disabled":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="账户已被禁用")

    return user


def require_role(*roles: str):
    """返回一个依赖，要求当前用户具有指定角色之一"""

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
        return current_user

    return role_checker


# 快捷依赖
get_current_admin = require_role("admin")
# 注意：角色已简化为 user 和 admin 两级
# - user: 聊天 + 管理自己的 AI 角色 + 查看统计
# - admin: 用户管理 + 审核 + 日志 + 系统统计（不参与聊天）
