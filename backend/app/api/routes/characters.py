"""AI 角色路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_manager, get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.ai_character import CharacterBrief, CharacterCreate, CharacterResponse, CharacterUpdate
from app.services.character_service import CharacterService
from app.utils.response import APIResponse

router = APIRouter()


# ==================== 公开/用户接口 ====================

@router.get("", summary="查看可用 AI 角色列表")
def list_characters(
    category: str | None = Query(None),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    """列出所有 active 状态的角色，支持按分类和名称搜索"""
    characters = CharacterService.list_active(db, category=category, search=search)
    return APIResponse.ok(data=[CharacterBrief.model_validate(c).model_dump() for c in characters])


@router.get("/{character_id}", summary="查看 AI 角色详情")
def get_character(
    character_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    character = CharacterService.get_by_id(db, character_id)
    return APIResponse.ok(data=CharacterResponse.model_validate(character).model_dump())


# ==================== 角色维护者/管理员接口 ====================

@router.post("", summary="创建 AI 角色")
def create_character(
    req: CharacterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    character = CharacterService.create(db, current_user, req)
    return APIResponse.created(data=CharacterResponse.model_validate(character).model_dump(), message="角色创建成功")


@router.put("/{character_id}", summary="更新 AI 角色")
def update_character(
    character_id: int,
    req: CharacterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    character = CharacterService.get_by_id(db, character_id)

    # 角色维护者只能编辑自己创建的角色，admin 可以编辑所有
    if current_user.role != "admin" and character.creator_id != current_user.id:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能编辑自己创建的角色")

    # 非 admin 不允许修改状态
    if req.status is not None and current_user.role != "admin":
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只有管理员可以修改角色状态")

    character = CharacterService.update(db, character, req)
    return APIResponse.ok(data=CharacterResponse.model_validate(character).model_dump(), message="更新成功")


@router.delete("/{character_id}", summary="删除 AI 角色")
def delete_character(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    character = CharacterService.get_by_id(db, character_id)

    if current_user.role != "admin" and character.creator_id != current_user.id:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能删除自己创建的角色")

    CharacterService.delete(db, character)
    return APIResponse.ok(message="角色已删除")


@router.put("/{character_id}/disable", summary="禁用 AI 角色")
def disable_character(
    character_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    character = CharacterService.get_by_id(db, character_id)
    character = CharacterService.disable(db, character)
    return APIResponse.ok(data=CharacterResponse.model_validate(character).model_dump(), message="角色已禁用")


# ==================== 统计与反馈 ====================

@router.get("/{character_id}/stats", summary="查看 AI 角色使用统计")
def get_character_stats(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    character = CharacterService.get_by_id(db, character_id)
    if current_user.role != "admin" and character.creator_id != current_user.id:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能查看自己创建角色的统计")

    from app.models.conversation import Conversation
    from app.models.feedback import Feedback
    from app.models.message import Message

    conv_count = db.query(Conversation).filter(Conversation.character_id == character_id).count()
    msg_count = db.query(Message).join(Conversation).filter(Conversation.character_id == character_id).count()
    like_count = db.query(Feedback).filter(
        Feedback.character_id == character_id, Feedback.feedback_type == "like"
    ).count()
    dislike_count = db.query(Feedback).filter(
        Feedback.character_id == character_id, Feedback.feedback_type == "dislike"
    ).count()

    return APIResponse.ok(data={
        "character_id": character_id,
        "character_name": character.name,
        "usage_count": character.usage_count,
        "conversation_count": conv_count,
        "message_count": msg_count,
        "like_count": like_count,
        "dislike_count": dislike_count,
    })


@router.get("/{character_id}/feedbacks", summary="查看 AI 角色收到的反馈")
def get_character_feedbacks(
    character_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    character = CharacterService.get_by_id(db, character_id)
    if current_user.role != "admin" and character.creator_id != current_user.id:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能查看自己创建角色的反馈")

    from app.models.feedback import Feedback
    query = db.query(Feedback).filter(Feedback.character_id == character_id)
    total = query.count()
    items = query.order_by(Feedback.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return APIResponse.paginated(
        items=[{
            "id": f.id,
            "user_id": f.user_id,
            "message_id": f.message_id,
            "feedback_type": f.feedback_type,
            "content": f.content,
            "tags": f.tags,
            "created_at": f.created_at.isoformat(),
        } for f in items],
        total=total,
        page=page,
        page_size=page_size,
    )
