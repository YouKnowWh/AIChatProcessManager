"""路由聚合"""

from app.api.routes import auth, users, conversations, messages  # noqa: F401
from app.api.routes import favorites, feedbacks, admin, logs, stats, context  # noqa: F401
