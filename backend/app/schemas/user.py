"""用户相关 Pydantic 模型"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    nickname: str | None
    avatar: str | None
    phone: str | None
    bio: str | None
    role: str
    status: str
    last_login_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    nickname: str | None = Field(None, max_length=50)
    avatar: str | None = Field(None, max_length=500)
    phone: str | None = Field(None, max_length=20)
    bio: str | None = None


class AdminUserUpdateRequest(UserUpdateRequest):
    role: str | None = Field(None, pattern="^(user|admin)$")
    status: str | None = Field(None, pattern="^(active|disabled)$")


class ResetPasswordRequest(BaseModel):
    new_password: str = Field(..., min_length=6, max_length=128)
