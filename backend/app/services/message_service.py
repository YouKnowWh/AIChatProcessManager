"""消息服务 — 消息发送、查询、删除"""

from datetime import datetime
import json
from uuid import uuid4

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
from app.services.log_service import LogService


class MessageService:
    @staticmethod
    def _emit_flow_terminal(trace_id: str, stage: str, table: str, summary: str, extra: dict | None = None):
        payload = {
            "trace_id": trace_id,
            "stage": stage,
            "table": table,
            "summary": summary,
        }
        if extra:
            payload["extra"] = extra
        print(f"[message_flow] {json.dumps(payload, ensure_ascii=False)}")

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
        trace_id = uuid4().hex[:8]
        flow_steps: list[dict] = []

        def record_flow(stage: str, table: str, summary: str, extra: dict | None = None):
            step = {
                "stage": stage,
                "table": table,
                "summary": summary,
            }
            if extra:
                step["extra"] = extra
            flow_steps.append(step)
            MessageService._emit_flow_terminal(trace_id, stage, table, summary, extra)

        # 1. 校验会话权限
        conversation = ConversationService.get_by_id(db, conversation_id, user)
        if conversation.status != "active":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="会话已归档或删除，无法发送消息")

        history_message_count = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).count()
        history_content_count = (
            db.query(MessageContent)
            .join(Message, Message.id == MessageContent.message_id)
            .filter(Message.conversation_id == conversation_id)
            .count()
        )
        record_flow(
            "context_loaded",
            "conversations/messages/message_contents",
            "Rebuild message context from conversation history",
            {
                "conversation_id": conversation_id,
                "history_messages": history_message_count,
                "history_content_blocks": history_content_count,
            },
        )

        # 2. 确定序列号
        max_seq = history_message_count

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
        record_flow(
            "write_user_message",
            "messages",
            "Insert user message row",
            {
                "message_id": user_msg.id,
                "sender_type": user_msg.sender_type,
                "role": user_msg.role,
                "sequence_number": user_msg.sequence_number,
            },
        )

        user_content = MessageContent(
            message_id=user_msg.id,
            content_type="text",
            content=content,
            sort_order=0,
        )
        db.add(user_content)
        db.flush()
        record_flow(
            "write_user_content",
            "message_contents",
            "Insert user content block",
            {
                "message_id": user_msg.id,
                "content_block_id": user_content.id,
                "content_type": user_content.content_type,
                "sort_order": user_content.sort_order,
                "content": content,
            },
        )

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
        record_flow(
            "write_ai_message",
            "messages",
            "Insert assistant message row",
            {
                "message_id": ai_msg.id,
                "parent_message_id": ai_msg.parent_message_id,
                "sender_type": ai_msg.sender_type,
                "role": ai_msg.role,
                "sequence_number": ai_msg.sequence_number,
            },
        )

        # 6. 保存 AI 回复内容
        ai_content = MessageContent(
            message_id=ai_msg.id,
            content_type="text",
            content=ai_result.content,
            sort_order=0,
        )
        db.add(ai_content)
        db.flush()
        record_flow(
            "write_ai_content",
            "message_contents",
            "Insert assistant content block",
            {
                "message_id": ai_msg.id,
                "content_block_id": ai_content.id,
                "content_type": ai_content.content_type,
                "sort_order": ai_content.sort_order,
                "content": ai_result.content,
            },
        )

        # 7. 保存推理过程
        reasoning = MessageReasoning(
            message_id=ai_msg.id,
            reasoning_content=ai_result.reasoning,
            visibility="owner_visible",
        )
        db.add(reasoning)
        db.flush()
        record_flow(
            "write_reasoning",
            "message_reasoning",
            "Insert reasoning block",
            {
                "message_id": ai_msg.id,
                "reasoning_id": reasoning.id,
                "visibility": reasoning.visibility,
                "content": ai_result.reasoning,
            },
        )

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
            record_flow(
                "write_tool_call",
                "tool_calls",
                "Insert tool call block",
                {
                    "message_id": ai_msg.id,
                    "tool_call_id": tool_call.id,
                    "tool_name": tool_call.tool_name,
                    "tool_type": tool_call.tool_type,
                    "status": tool_call.status,
                },
            )

            # 保存工具结果
            if i < len(ai_result.tool_results):
                tr_data = ai_result.tool_results[i]
                tool_result = ToolResult(
                    tool_call_id=tool_call.id,
                    result_content=tr_data["result_content"],
                    is_error=tr_data["is_error"],
                )
                db.add(tool_result)
                db.flush()
                record_flow(
                    "write_tool_result",
                    "tool_results",
                    "Insert tool result block",
                    {
                        "tool_call_id": tool_call.id,
                        "tool_result_id": tool_result.id,
                        "is_error": tool_result.is_error,
                    },
                )

                # 记录工具调用日志
                LogService.write(
                    db, action="tool_call", user_id=user.id,
                    target_type="tool_call", target_id=tool_call.id,
                    detail=json.dumps({"message_id": ai_msg.id, "tool_name": tc_data["tool_name"], "tool_type": tc_data["tool_type"], "status": tc_data["status"]}, ensure_ascii=False),
                )

        # 模拟知识库调用记录（查阅用户的知识库）
        from app.models.knowledge_entry import KnowledgeEntry
        knowledge_entries = db.query(KnowledgeEntry).filter(
            KnowledgeEntry.user_id == user.id,
            KnowledgeEntry.status == "active",
        ).limit(3).all()
        if knowledge_entries:
            for ke in knowledge_entries:
                LogService.write(
                    db, action="knowledge_call", user_id=user.id,
                    target_type="knowledge_entry", target_id=ke.id,
                    detail=json.dumps({"message_id": ai_msg.id, "entry_title": ke.title}, ensure_ascii=False),
                )
            record_flow(
                "knowledge_lookup",
                "knowledge_entries",
                "Simulated knowledge base lookup",
                {"user_id": user.id, "entries_found": len(knowledge_entries)},
            )

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
        db.flush()
        record_flow(
            "write_metadata",
            "message_metadata",
            "Insert model metadata block",
            {
                "message_id": ai_msg.id,
                "metadata_id": metadata.id,
                "model_name": metadata.model_name,
                "provider": metadata.provider,
                "total_tokens": metadata.total_tokens,
                "duration_ms": metadata.duration_ms,
            },
        )

        # 10. 更新角色使用次数
        CharacterService.increment_usage(db, character)

        # 11. 更新最后消息时间
        ConversationService.touch_last_message(db, conversation)

        # 12. 记录系统日志
        LogService.write(
            db, action="send_message", user_id=user.id,
            target_type="message", target_id=user_msg.id,
            detail=json.dumps({"conversation_id": conversation_id, "ai_message_id": ai_msg.id, "has_tools": len(ai_result.tool_calls) > 0}, ensure_ascii=False),
        )

        # 13. 构建上下文片段并建立引用
        from app.services.context_service import ContextService
        segment = ContextService.build_recent_context(
            db, conversation_id, user.id, ai_msg.id, max_messages=5
        )
        if segment:
            ContextService.link_message_context(db, ai_msg.id, segment.id, ref_type="used")
            LogService.write(
                db, action="create_context_segment", user_id=user.id,
                target_type="context_segment", target_id=segment.id,
                detail=json.dumps({"message_id": ai_msg.id, "token_count": segment.token_count, "messages": segment.start_message_id}, ensure_ascii=False),
            )
            LogService.write(
                db, action="link_message_context", user_id=user.id,
                target_type="message_context_refs", target_id=ai_msg.id,
                detail=json.dumps({"context_segment_id": segment.id, "ref_type": "used"}, ensure_ascii=False),
            )

        db.commit()
        record_flow(
            "write_log",
            "system_logs",
            "Insert system log row and commit transaction",
            {
                "user_message_id": user_msg.id,
                "ai_message_id": ai_msg.id,
                "tool_call_count": len(ai_result.tool_calls),
            },
        )
        LogService.write(
            db,
            action="message_flow_trace",
            user_id=user.id,
            target_type="conversation",
            target_id=conversation_id,
            detail=json.dumps({
                "trace_id": trace_id,
                "conversation_id": conversation_id,
                "user_message_id": user_msg.id,
                "ai_message_id": ai_msg.id,
                "character_id": character.id,
                "character_name": character.name,
                "user_content": content,
                "ai_content_preview": ai_result.content,
                "model": ai_result.model_name,
                "total_tokens": ai_result.total_tokens,
                "duration_ms": ai_result.duration_ms,
                "steps": flow_steps,
            }, ensure_ascii=False),
        )

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
