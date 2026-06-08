"""系统日志服务"""

from sqlalchemy.orm import Session

from app.models.system_log import SystemLog


class LogService:

    @staticmethod
    def write(
        db: Session,
        action: str,
        user_id: int | None = None,
        target_type: str | None = None,
        target_id: int | None = None,
        detail: str | None = None,
        ip_address: str | None = None,
    ) -> SystemLog:
        """记录一条系统日志"""
        log = SystemLog(
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            detail=detail,
            ip_address=ip_address,
        )
        db.add(log)
        db.commit()
        return log

    @staticmethod
    def list_by_admin(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        user_id: int | None = None,
        action: str | None = None,
        target_type: str | None = None,
    ):
        """管理员查询日志"""
        query = db.query(SystemLog)
        if user_id:
            query = query.filter(SystemLog.user_id == user_id)
        if action:
            query = query.filter(SystemLog.action == action)
        if target_type:
            query = query.filter(SystemLog.target_type == target_type)

        total = query.count()
        items = (
            query
            .order_by(SystemLog.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total
