"""消息路由 — 发送、列表、详情、搜索、删除、过程数据查询"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.message import MessageSendRequest
from app.services.message_service import MessageService
from app.utils.response import APIResponse

router = APIRouter()


# ==================== 用户消息接口 ====================

@router.get("/conversations/{conversation_id}/messages", summary="获取会话消息列表")
def list_messages(
    conversation_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = MessageService.list_by_conversation(
        db, conversation_id, current_user, page=page, page_size=page_size
    )
    return APIResponse.paginated(items=items, total=total, page=page, page_size=page_size)


@router.post("/conversations/{conversation_id}/messages", summary="发送消息（触发 AI 回复）")
def send_message(
    conversation_id: int,
    req: MessageSendRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = MessageService.send_message(db, conversation_id, current_user, req.content)
    return APIResponse.created(data=result, message="消息发送成功")


@router.get("/messages/{message_id}", summary="查看消息（含 content）")
def get_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    detail = MessageService.get_message_detail(db, message_id, current_user)
    return APIResponse.ok(data=detail)


@router.get("/messages/{message_id}/detail", summary="查看消息完整详情（含过程数据）")
def get_message_detail(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """完整展示 reasoning、tool_calls、tool_results、metadata"""
    detail = MessageService.get_message_detail(db, message_id, current_user)
    return APIResponse.ok(data=detail)


@router.get("/messages/search", summary="搜索消息")
def search_messages(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = MessageService.search_messages(db, current_user, keyword, page=page, page_size=page_size)
    return APIResponse.paginated(items=items, total=total, page=page, page_size=page_size)


@router.delete("/messages/{message_id}", summary="删除消息（软删除）")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    MessageService.soft_delete_message(db, message_id, current_user)
    return APIResponse.ok(message="消息已删除")


# ==================== 消息过程数据独立查询 ====================

@router.get("/messages/{message_id}/contents", summary="查看消息正文块")
def get_message_contents(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    detail = MessageService.get_message_detail(db, message_id, current_user)
    return APIResponse.ok(data=detail["contents"])


@router.get("/messages/{message_id}/reasoning", summary="查看推理过程")
def get_message_reasoning(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    detail = MessageService.get_message_detail(db, message_id, current_user)
    reasoning = detail.get("reasoning")
    if not reasoning:
        return APIResponse.ok(data=None, message="该消息没有推理过程")
    # 非 AI 消息或 owner/admin 不可见的隐藏推理
    if reasoning["visibility"] == "hidden" and current_user.role != "admin":
        return APIResponse.fail(code=403, message="推理过程不可见")
    return APIResponse.ok(data=reasoning)


@router.get("/messages/{message_id}/tool-calls", summary="查看工具调用记录")
def get_message_tool_calls(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    detail = MessageService.get_message_detail(db, message_id, current_user)
    return APIResponse.ok(data=detail["tool_calls"])


@router.get("/messages/{message_id}/metadata", summary="查看模型调用元数据")
def get_message_metadata(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    detail = MessageService.get_message_detail(db, message_id, current_user)
    return APIResponse.ok(data=detail["metadata"])


# ==================== 管理员消息管理 ====================

@router.get("/admin/messages", summary="管理员查看所有消息")
def admin_list_messages(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = Query(None, pattern="^(normal|hidden|deleted)$"),
    sender_type: str | None = Query(None, pattern="^(user|ai|system|tool)$"),
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    from app.models.message import Message as Msg
    query = db.query(Msg)
    if status:
        query = query.filter(Msg.status == status)
    if sender_type:
        query = query.filter(Msg.sender_type == sender_type)
    total = query.count()
    messages = query.order_by(Msg.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    items = [{"id": m.id, "conversation_id": m.conversation_id, "sender_type": m.sender_type,
              "role": m.role, "status": m.status, "sequence_number": m.sequence_number,
              "created_at": m.created_at.isoformat()} for m in messages]
    return APIResponse.paginated(items=items, total=total, page=page, page_size=page_size)


@router.put("/admin/messages/{message_id}/hide", summary="管理员隐藏消息")
def hide_message(
    message_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    from app.models.message import Message as Msg
    msg = db.query(Msg).filter(Msg.id == message_id).first()
    if not msg:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="消息不存在")
    msg.status = "hidden"
    db.commit()
    return APIResponse.ok(message="消息已隐藏")


@router.put("/admin/messages/{message_id}/restore", summary="管理员恢复消息")
def restore_message(
    message_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    from app.models.message import Message as Msg
    msg = db.query(Msg).filter(Msg.id == message_id).first()
    if not msg:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="消息不存在")
    msg.status = "normal"
    db.commit()
    return APIResponse.ok(message="消息已恢复")
