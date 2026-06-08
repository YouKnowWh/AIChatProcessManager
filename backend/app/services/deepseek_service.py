"""DeepSeek API 服务 — 接入真实 DeepSeek flash 模型"""

import time
import traceback
from dataclasses import dataclass, field

import httpx

from app.core.config import settings


@dataclass
class AIResult:
    """AI 回复的完整结果（统一格式，兼容 fake_ai_service）"""
    content: str
    reasoning: str = ""
    tool_calls: list[dict] = field(default_factory=list)
    tool_results: list[dict] = field(default_factory=list)
    model_name: str = "deepseek-v4-flash"
    provider: str = "deepseek"
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    duration_ms: int = 0
    finish_reason: str = "stop"


class DeepSeekService:
    """DeepSeek API 调用服务（OpenAI 兼容接口）"""

    BASE_URL = "https://api.deepseek.com/v1"
    MODEL = "deepseek-chat"  # deepseek-chat → deepseek-v4-flash

    @classmethod
    def generate(
        cls,
        user_content: str,
        character_name: str,
        character_prompt: str | None = None,
    ) -> AIResult:
        """调用 DeepSeek API 生成回复（同步版本）"""
        api_key = settings.DEEPSEEK_API_KEY
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY 未配置")

        system_prompt = character_prompt or f"你是{character_name}，一个 AI 助手。请用中文友好地回答用户的问题。"
        if character_prompt:
            system_prompt = f"{character_prompt}\n\n你的名字是：{character_name}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]

        start_time = time.time()

        response = httpx.post(
            f"{cls.BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": cls.MODEL,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 4096,
            },
            timeout=60.0,
        )

        duration_ms = int((time.time() - start_time) * 1000)

        if response.status_code != 200:
            error_detail = response.text[:500]
            raise RuntimeError(f"DeepSeek API 返回 {response.status_code}: {error_detail}")

        data = response.json()

        try:
            choice = data["choices"][0]
            msg = choice.get("message", {})
            content = msg.get("content", "") or "（模型未返回内容）"
            finish_reason = choice.get("finish_reason", "stop")

            usage = data.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)

            # 使用 API 返回的实际模型名（deepseek-chat → deepseek-v4-flash）
            actual_model = data.get("model", cls.MODEL)

            # deepseek-chat (flash) 没有 reasoning_content，只有 deepseek-reasoner 有
            reasoning_content = msg.get("reasoning_content", "")

            return AIResult(
                content=content,
                reasoning=reasoning_content,
                model_name=actual_model,
                provider="deepseek",
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                duration_ms=duration_ms,
                finish_reason=finish_reason,
            )
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"DeepSeek API 返回数据格式异常: {e}") from e

    @classmethod
    def generate_safe(
        cls,
        user_content: str,
        character_name: str,
        character_prompt: str | None = None,
    ) -> AIResult:
        """生成回复，失败时回退到模拟服务"""
        try:
            return cls.generate(user_content, character_name, character_prompt)
        except Exception as e:
            from app.services.fake_ai_service import FakeAIService
            print(f"[DeepSeek] API 调用失败，回退到 FakeAIService: {e}")
            traceback.print_exc()
            fake = FakeAIService.generate(user_content, character_name, character_prompt)
            return AIResult(
                content=f"⚠️ DeepSeek API 暂时不可用（{e}），以下是模拟回复：\n\n{fake.content}",
                reasoning=f"[回退模式] 原因: {e}\n{fake.reasoning}",
                tool_calls=fake.tool_calls,
                tool_results=fake.tool_results,
                model_name=fake.model_name,
                provider=fake.provider,
                prompt_tokens=fake.prompt_tokens,
                completion_tokens=fake.completion_tokens,
                total_tokens=fake.total_tokens or 0,
                duration_ms=fake.duration_ms,
                finish_reason="error",
            )
