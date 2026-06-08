"""审核记录服务"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.audit_record import AuditRecord
from app.models.user import User


class AuditService:

    @staticmethod
    def create(db: Session, admin: User, target_type: str, target_id: int,
               action: str, comment: str | None = None) -> AuditRecord:
        """创建审核记录"""
        record = AuditRecord(
            admin_id=admin.id,
            target_type=target_type,
            target_id=target_id,
            action=action,
            comment=comment,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def list_by_admin(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        target_type: str | None = None,
        action: str | None = None,
    ):
        """管理员查询审核记录"""
        query = db.query(AuditRecord)
        if target_type:
            query = query.filter(AuditRecord.target_type == target_type)
        if action:
            query = query.filter(AuditRecord.action == action)

        total = query.count()
        items = (
            query
            .order_by(AuditRecord.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total
