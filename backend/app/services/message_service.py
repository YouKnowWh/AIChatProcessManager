"""消息服务 — 消息发送、查询、删除"""

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.conversation import Conversation
from app.models.message import Message
from app.models.message_content import MessageContent
from app.models.favorite import MessageFavorite
from app.models.message_metadata import MessageMetadata
from app.models.message_reasoning import MessageReasoning
from app.models.tool_call import ToolCall
from app.models.tool_result import ToolResult
from app.models.user import User
from app.services.conversation_service import ConversationService
from app.services.character_service import CharacterService
from app.services.deepseek_service import DeepSeekService


class MessageService:

    @staticmethod
    def list_by_conversation(db: Session, conversation_id: int, user: User,
                             page: int = 1, page_size: int = 50):
        """获取会话的消息列表（只返回 content，不含过程数据）"""
        conversation = ConversationService.get_by_id(db, conversation_id, user)

        query = db.query(Message).filter(
            Message.conversation_id == conversation_id,
            Message.status.in_(["normal"]),  # 默认不返回 hidden/deleted
        )
        total = query.count()
        messages = (
            query
            .options(joinedload(Message.contents))
            .order_by(Message.sequence_number.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        message_ids = [msg.id for msg in messages]
        favorite_ids = set()
        if message_ids:
            favorite_ids = {
                row[0]
                for row in db.query(MessageFavorite.message_id)
                .filter(
                    MessageFavorite.user_id == user.id,
                    MessageFavorite.message_id.in_(message_ids),
                )
                .all()
            }

        items = []
        for msg in messages:
            items.append({
                "id": msg.id,
                "conversation_id": msg.conversation_id,
                "parent_message_id": msg.parent_message_id,
                "sender_type": msg.sender_type,
                "role": msg.role,
                "status": msg.status,
                "sequence_number": msg.sequence_number,
                "created_at": msg.created_at.isoformat(),
                "is_favorited": msg.id in favorite_ids,
                "contents": [
                    {
                        "id": c.id,
                        "content_type": c.content_type,
                        "content": c.content,
                        "sort_order": c.sort_order,
                    }
                    for c in sorted(msg.contents, key=lambda x: x.sort_order)
                ],
            })

        return items, total

    @staticmethod
    def send_message(db: Session, conversation_id: int, user: User, content: str):
        """发送消息并触发模拟 AI 回复"""
        # 1. 校验会话权限
        conversation = ConversationService.get_by_id(db, conversation_id, user)
        if conversation.status != "active":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="会话已归档或删除，无法发送消息")

        # 2. 确定序列号
        max_seq = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).count()

        # 3. 保存用户消息
        user_msg = Message(
            conversation_id=conversation_id,
            parent_message_id=None,
            sender_type="user",
            role="user",
            status="normal",
            sequence_number=max_seq + 1,
        )
        db.add(user_msg)
        db.flush()

        user_content = MessageContent(
            message_id=user_msg.id,
            content_type="text",
            content=content,
            sort_order=0,
        )
        db.add(user_content)

        # 更新最后消息时间
        ConversationService.touch_last_message(db, conversation)

        # 4. 调用 AI 服务（DeepSeek 真实 API，失败自动回退 FakeAI）
        character = conversation.character
        ai_result = DeepSeekService.generate_safe(
            user_content=content,
            character_name=character.name,
            character_prompt=character.system_prompt,
        )

        # 5. 保存 AI 回复消息
        ai_msg = Message(
            conversation_id=conversation_id,
            parent_message_id=user_msg.id,
            sender_type="ai",
            role="assistant",
            status="normal",
            sequence_number=max_seq + 2,
        )
        db.add(ai_msg)
        db.flush()

        # 6. 保存 AI 回复内容
        ai_content = MessageContent(
            message_id=ai_msg.id,
            content_type="text",
            content=ai_result.content,
            sort_order=0,
        )
        db.add(ai_content)

        # 7. 保存推理过程
        reasoning = MessageReasoning(
            message_id=ai_msg.id,
            reasoning_content=ai_result.reasoning,
            visibility="owner_visible",
        )
        db.add(reasoning)

        # 8. 保存工具调用和结果
        for i, tc_data in enumerate(ai_result.tool_calls):
            tool_call = ToolCall(
                message_id=ai_msg.id,
                tool_name=tc_data["tool_name"],
                tool_type=tc_data["tool_type"],
                arguments=tc_data["arguments"],
                call_id=tc_data["call_id"],
                status=tc_data["status"],
                called_at=datetime.now(),
                completed_at=datetime.now(),
            )
            db.add(tool_call)
            db.flush()

            # 保存工具结果
            if i < len(ai_result.tool_results):
                tr_data = ai_result.tool_results[i]
                tool_result = ToolResult(
                    tool_call_id=tool_call.id,
                    result_content=tr_data["result_content"],
                    is_error=tr_data["is_error"],
                )
                db.add(tool_result)

        # 9. 保存元数据
        metadata = MessageMetadata(
            message_id=ai_msg.id,
            model_name=ai_result.model_name,
            provider=ai_result.provider,
            prompt_tokens=ai_result.prompt_tokens,
            completion_tokens=ai_result.completion_tokens,
            total_tokens=ai_result.total_tokens,
            duration_ms=ai_result.duration_ms,
            finish_reason=ai_result.finish_reason,
            temperature=0.70,
            top_p=0.90,
        )
        db.add(metadata)

        # 10. 更新角色使用次数
        CharacterService.increment_usage(db, character)

        # 11. 更新最后消息时间
        ConversationService.touch_last_message(db, conversation)

        db.commit()

        # 重新加载完整数据返回
        return MessageService._build_response(db, user_msg, ai_msg)

    @staticmethod
    def get_message_detail(db: Session, message_id: int, user: User):
        """获取消息完整详情（含所有过程数据）"""
        msg = db.query(Message).filter(Message.id == message_id).first()
        if not msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="消息不存在")

        # 权限：只能看自己会话的消息，或 admin
        conversation = msg.conversation
        if conversation.user_id != user.id and user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权查看该消息")

        return MessageService._build_detail(msg)

    @staticmethod
    def search_messages(db: Session, user: User, keyword: str,
                        page: int = 1, page_size: int = 20):
        """搜索当前用户的消息（按 content 关键词）"""
        from app.models.conversation import Conversation as Conv
        user_conv_ids = db.query(Conv.id).filter(Conv.user_id == user.id).subquery()

        query = (
            db.query(Message)
            .join(MessageContent, MessageContent.message_id == Message.id)
            .filter(
                Message.conversation_id.in_(user_conv_ids),
                Message.status == "normal",
                MessageContent.content.contains(keyword),
            )
        )
        total = query.count()
        messages = (
            query
            .options(joinedload(Message.contents))
            .order_by(Message.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        items = []
        for msg in messages:
            items.append({
                "id": msg.id,
                "conversation_id": msg.conversation_id,
                "sender_type": msg.sender_type,
                "role": msg.role,
                "sequence_number": msg.sequence_number,
                "created_at": msg.created_at.isoformat(),
                "contents": [
                    {"id": c.id, "content_type": c.content_type, "content": c.content, "sort_order": c.sort_order}
                    for c in sorted(msg.contents, key=lambda x: x.sort_order)
                ],
            })

        return items, total

    @staticmethod
    def soft_delete_message(db: Session, message_id: int, user: User):
        """软删除消息"""
        msg = db.query(Message).filter(Message.id == message_id).first()
        if not msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="消息不存在")

        conversation = msg.conversation
        if conversation.user_id != user.id and user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权删除该消息")

        msg.status = "deleted"
        db.commit()

    @staticmethod
    def _build_response(db: Session, user_msg: Message, ai_msg: Message) -> dict:
        """构建发送消息的返回数据"""
        db.refresh(user_msg)
        db.refresh(ai_msg)
        return {
            "user_message": {
                "id": user_msg.id,
                "conversation_id": user_msg.conversation_id,
                "sender_type": user_msg.sender_type,
                "role": user_msg.role,
                "sequence_number": user_msg.sequence_number,
                "created_at": user_msg.created_at.isoformat(),
                "contents": [
                    {"id": c.id, "content_type": c.content_type, "content": c.content, "sort_order": c.sort_order}
                    for c in sorted(user_msg.contents, key=lambda x: x.sort_order)
                ],
            },
            "ai_message": {
                "id": ai_msg.id,
                "conversation_id": ai_msg.conversation_id,
                "sender_type": ai_msg.sender_type,
                "role": ai_msg.role,
                "sequence_number": ai_msg.sequence_number,
                "created_at": ai_msg.created_at.isoformat(),
                "contents": [
                    {"id": c.id, "content_type": c.content_type, "content": c.content, "sort_order": c.sort_order}
                    for c in sorted(ai_msg.contents, key=lambda x: x.sort_order)
                ],
            },
        }

    @staticmethod
    def _build_detail(msg: Message) -> dict:
        """构建消息完整详情"""
        result = {
            "message": {
                "id": msg.id,
                "conversation_id": msg.conversation_id,
                "parent_message_id": msg.parent_message_id,
                "sender_type": msg.sender_type,
                "role": msg.role,
                "status": msg.status,
                "sequence_number": msg.sequence_number,
                "created_at": msg.created_at.isoformat(),
            },
            "contents": [
                {"id": c.id, "content_type": c.content_type, "content": c.content, "sort_order": c.sort_order}
                for c in sorted(msg.contents, key=lambda x: x.sort_order)
            ],
            "reasoning": None,
            "tool_calls": [],
            "metadata": None,
        }

        # 推理过程
        if msg.reasoning:
            result["reasoning"] = {
                "id": msg.reasoning.id,
                "reasoning_content": msg.reasoning.reasoning_content,
                "visibility": msg.reasoning.visibility,
            }

        # 工具调用 + 结果
        for tc in msg.tool_calls:
            tc_block = {
                "id": tc.id,
                "tool_name": tc.tool_name,
                "tool_type": tc.tool_type,
                "arguments": tc.arguments,
                "call_id": tc.call_id,
                "status": tc.status,
                "result": None,
            }
            if tc.result:
                tc_block["result"] = {
                    "id": tc.result.id,
                    "result_content": tc.result.result_content,
                    "is_error": tc.result.is_error,
                }
            result["tool_calls"].append(tc_block)

        # 元数据
        if msg.model_metadata:
            result["metadata"] = {
                "id": msg.model_metadata.id,
                "model_name": msg.model_metadata.model_name,
                "provider": msg.model_metadata.provider,
                "prompt_tokens": msg.model_metadata.prompt_tokens,
                "completion_tokens": msg.model_metadata.completion_tokens,
                "total_tokens": msg.model_metadata.total_tokens,
                "duration_ms": msg.model_metadata.duration_ms,
                "finish_reason": msg.model_metadata.finish_reason,
                "temperature": float(msg.model_metadata.temperature) if msg.model_metadata.temperature else None,
                "top_p": float(msg.model_metadata.top_p) if msg.model_metadata.top_p else None,
            }

        return result
