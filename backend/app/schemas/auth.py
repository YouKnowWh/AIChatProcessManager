"""认证相关 Pydantic 模型"""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["user1"])
    email: EmailStr = Field(..., examples=["user1@example.com"])
    password: str = Field(..., min_length=6, max_length=128, examples=["user123"])
    nickname: str | None = Field(None, max_length=50)


class LoginRequest(BaseModel):
    username: str = Field(..., examples=["user1"])
    password: str = Field(..., examples=["user123"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserBrief"


class UserBrief(BaseModel):
    id: int
    username: str
    email: str
    nickname: str | None
    role: str
    avatar: str | None

    model_config = {"from_attributes": True}
