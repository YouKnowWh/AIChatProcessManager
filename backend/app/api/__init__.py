"""路由聚合"""

from app.api.routes import auth, users, characters, conversations, messages  # noqa: F401
from app.api.routes import favorites, feedbacks, admin, logs, stats  # noqa: F401
