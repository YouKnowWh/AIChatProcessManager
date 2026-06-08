"""FastAPI 应用入口"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["系统"])
def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}


# 路由注册（后续逐步添加）
from app.api.routes import auth, users, characters, conversations, messages  # noqa: E402
from app.api.routes import favorites, feedbacks, admin, logs, stats  # noqa: E402

app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api", tags=["用户"])
app.include_router(characters.router, prefix="/api/characters", tags=["AI 角色"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["会话"])
app.include_router(messages.router, prefix="/api", tags=["消息"])
app.include_router(favorites.router, prefix="/api", tags=["收藏"])
app.include_router(feedbacks.router, prefix="/api", tags=["反馈"])
app.include_router(admin.router, prefix="/api/admin", tags=["管理员"])
app.include_router(logs.router, prefix="/api/admin/logs", tags=["系统日志"])
app.include_router(stats.router, prefix="/api/stats", tags=["统计"])
