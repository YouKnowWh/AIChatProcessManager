"""模拟 AI 回复服务 — 不接入真实大模型 API，生成完整的过程链路数据"""

import hashlib
import random
import time
from dataclasses import dataclass, field


@dataclass
class FakeAIResult:
    """模拟 AI 回复的完整结果"""
    content: str
    reasoning: str
    tool_calls: list[dict] = field(default_factory=list)
    tool_results: list[dict] = field(default_factory=list)
    model_name: str = "claude-sonnet-4-6"
    provider: str = "anthropic"
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    duration_ms: int = 0
    finish_reason: str = "stop"


class FakeAIService:
    """根据用户消息内容和 AI 角色，生成模拟的完整 AI 回复过程链路"""

    MODEL_POOL = [
        {"name": "claude-sonnet-4-6", "provider": "anthropic"},
        {"name": "claude-opus-4-8", "provider": "anthropic"},
        {"name": "gpt-4o", "provider": "openai"},
        {"name": "deepseek-v3", "provider": "deepseek"},
    ]

    TOOL_DEFINITIONS = {
        "search": {"name": "web_search", "type": "search", "desc": "搜索网络信息"},
        "database": {"name": "query_database", "type": "database", "desc": "查询数据库"},
        "calculator": {"name": "calculate", "type": "calculator", "desc": "执行计算"},
        "file": {"name": "read_file", "type": "file", "desc": "读取文件内容"},
        "api": {"name": "call_api", "type": "api", "desc": "调用外部 API"},
    }

    @classmethod
    def generate(cls, user_content: str, character_name: str, character_prompt: str | None = None) -> FakeAIResult:
        """根据用户消息和角色信息生成模拟 AI 回复"""
        start_time = time.time()

        # 选择模型
        model = random.choice(cls.MODEL_POOL)

        # 判断是否需要工具调用
        needs_tools = cls._detect_tool_need(user_content)

        # 生成 reasoning
        reasoning = cls._generate_reasoning(user_content, character_name)

        # 生成正式回复
        content = cls._generate_content(user_content, character_name)

        # 生成工具调用
        tool_calls = []
        tool_results = []
        finish_reason = "stop"

        if needs_tools:
            tools_to_use = cls._pick_tools(user_content)
            for tc in tools_to_use:
                raw = f"{user_content}{tc['name']}"
                call_id = f"call_{hashlib.md5(raw.encode()).hexdigest()[:12]}"
                tool_calls.append({
                    "tool_name": tc["name"],
                    "tool_type": tc["type"],
                    "arguments": cls._generate_arguments(tc["type"], user_content),
                    "call_id": call_id,
                    "status": "success",
                })
                tool_results.append({
                    "result_content": cls._generate_tool_result(tc["type"], user_content),
                    "is_error": False,
                })
            finish_reason = "tool_calls"

        # token 估算
        prompt_tokens = cls._estimate_tokens(user_content + (character_prompt or ""))
        completion_tokens = cls._estimate_tokens(content + reasoning)

        # 模拟耗时 (500ms ~ 3500ms)
        duration_ms = int((time.time() - start_time) * 1000) + random.randint(300, 3000)

        return FakeAIResult(
            content=content,
            reasoning=reasoning,
            tool_calls=tool_calls,
            tool_results=tool_results,
            model_name=model["name"],
            provider=model["provider"],
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            duration_ms=duration_ms,
            finish_reason=finish_reason,
        )

    @classmethod
    def _detect_tool_need(cls, content: str) -> bool:
        """检测是否需要工具调用"""
        tool_keywords = ["搜索", "查一下", "查查", "搜索一下", "帮我找", "查询",
                         "计算", "算一下", "等于多少",
                         "天气", "新闻", "最新", "今天",
                         "文件", "读取", "打开",
                         "数据库", "数据",
                         "当前时间", "日期"]
        return any(kw in content for kw in tool_keywords)

    @classmethod
    def _pick_tools(cls, content: str) -> list[dict]:
        """根据内容选择合适的工具"""
        tools = []
        if any(kw in content for kw in ["搜索", "查一下", "查查", "搜索一下", "帮我找", "天气", "新闻", "最新"]):
            tools.append(cls.TOOL_DEFINITIONS["search"])
        if any(kw in content for kw in ["计算", "算一下", "等于多少"]):
            tools.append(cls.TOOL_DEFINITIONS["calculator"])
        if any(kw in content for kw in ["数据库", "数据", "查询"]):
            tools.append(cls.TOOL_DEFINITIONS["database"])
        if any(kw in content for kw in ["文件", "读取", "打开"]):
            tools.append(cls.TOOL_DEFINITIONS["file"])
        if not tools:
            tools.append(cls.TOOL_DEFINITIONS["search"])
        return tools[:2]  # 最多 2 个工具调用

    @classmethod
    def _generate_arguments(cls, tool_type: str, content: str) -> dict:
        """为工具生成模拟参数"""
        if tool_type == "search":
            return {"query": content[:60], "limit": random.randint(3, 10), "language": "zh"}
        elif tool_type == "calculator":
            return {"expression": "100 * (1 + 0.05) ** 5", "precision": 2}
        elif tool_type == "database":
            return {"table": "knowledge_base", "query": content[:40], "top_k": 5}
        elif tool_type == "file":
            return {"path": "/data/knowledge.txt", "encoding": "utf-8", "max_lines": 500}
        return {"query": content[:50]}

    @classmethod
    def _generate_tool_result(cls, tool_type: str, content: str) -> dict:
        """生成模拟工具结果"""
        if tool_type == "search":
            return {
                "results": [
                    {"title": f"关于「{content[:20]}」的搜索结果 1", "url": "https://example.com/1", "snippet": "相关内容摘要..."},
                    {"title": f"关于「{content[:20]}」的搜索结果 2", "url": "https://example.com/2", "snippet": "更多相关信息..."},
                ],
                "total_found": 42,
                "search_time_ms": random.randint(80, 400),
            }
        elif tool_type == "calculator":
            return {"result": round(random.uniform(1, 1000), 2), "expression": "100 * (1+0.05)^5", "steps": ["Step 1: ...", "Step 2: ..."]}
        elif tool_type == "database":
            return {"rows": [{"id": 1, "content": "数据行 1"}, {"id": 2, "content": "数据行 2"}], "query_time_ms": random.randint(5, 50)}
        elif tool_type == "file":
            return {"content_preview": "文件内容预览（前 500 行）...", "total_lines": 2340, "encoding": "utf-8"}
        return {"status": "ok", "data": {}}

    @classmethod
    def _generate_reasoning(cls, user_content: str, character_name: str) -> str:
        """生成模拟推理过程"""
        templates = [
            f"用户问了关于「{user_content[:30]}」的问题。我需要先理解用户的核心需求。"
            f"作为{character_name}，我应该从专业角度给出准确且实用的回答。"
            f"考虑到用户可能是初学者，回复应该包含足够的解释和示例。"
            f"决定采用结构化回复，先概述再详细展开，确保逻辑清晰。",

            f"收到用户消息：「{user_content[:30]}...」"
            f"这个问题可以从多个角度来回答。首先判断问题的复杂度——属于中等难度。"
            f"作为{character_name}，我可以提供具体的操作步骤。"
            f"但需要注意回复长度，避免信息过载。决定采用分点回答的方式，并在最后给出总结。",

            f"分析用户意图：基于「{user_content[:30]}」，用户可能在寻求帮助。"
            f"我应该：1) 确认理解了用户的意图 2) 提供针对性的解决方案 3) 给出进一步探索的方向。"
            f"回复风格应当友好且专业，符合{character_name}的定位。"
            f"如果涉及代码，要确保代码可以直接运行。",
        ]
        return random.choice(templates)

    @classmethod
    def _generate_content(cls, user_content: str, character_name: str) -> str:
        """根据用户消息生成模拟 AI 正式回复"""
        # 关键词驱动的回复生成
        content_lower = user_content.lower()

        if any(kw in content_lower for kw in ["你好", "hello", "hi", "嗨"]):
            return (
                f"你好！我是{character_name}，很高兴为你服务。\n\n"
                f"我可以帮你处理各种问题，包括：\n"
                f"- 📝 写作与编辑\n"
                f"- 💻 编程与代码审查\n"
                f"- 🔍 信息查询与搜索\n"
                f"- 📊 数据分析与整理\n"
                f"- 🌐 翻译与语言处理\n\n"
                f"请随时告诉我你需要的帮助！"
            )

        if any(kw in content_lower for kw in ["代码", "编程", "python", "函数", "写一个"]):
            return (
                f"好的，我来帮你处理这个编程问题。\n\n"
                f"```python\n"
                f"# 这是根据你的需求生成的示例代码\n"
                f"def process_data(data: list) -> list:\n"
                f'    """处理输入数据并返回结果"""\n'
                f"    result = []\n"
                f"    for item in data:\n"
                f"        # 进行相关处理\n"
                f"        processed = str(item).strip().lower()\n"
                f"        result.append(processed)\n"
                f"    return result\n"
                f"\n"
                f"# 使用示例\n"
                f"if __name__ == '__main__':\n"
                f"    sample = ['Apple', 'Banana', 'Cherry']\n"
                f"    output = process_data(sample)\n"
                f"    print(output)\n"
                f"```\n\n"
                f"**代码说明：**\n\n"
                f"1. `process_data` 函数接收一个列表作为输入\n"
                f"2. 遍历每个元素进行字符串处理\n"
                f"3. 返回处理后的结果列表\n\n"
                f"如果你需要其他编程语言或更具体的实现，请告诉我！"
            )

        if any(kw in content_lower for kw in ["翻译", "translate"]):
            return (
                f"好的，翻译如下：\n\n"
                f"**原文：**\n> {user_content}\n\n"
                f"**译文（英文）：**\n> This is a simulated translation result. "
                f"The original text has been translated according to its context and nuance.\n\n"
                f"如果需要其他语言方向（日文、韩文等），请告诉我。"
            )

        if any(kw in content_lower for kw in ["天气", "weather"]):
            return (
                f"根据查询结果，今天的天气情况如下：\n\n"
                f"| 指标 | 数值 |\n"
                f"|------|------|\n"
                f"| 温度 | {random.randint(18, 35)}°C |\n"
                f"| 湿度 | {random.randint(30, 80)}% |\n"
                f"| 风力 | {random.choice(['微风', '和风', '清风'])} {random.randint(1, 5)} 级 |\n"
                f"| 天气 | {random.choice(['晴', '多云', '阴', '小雨'])} |\n\n"
                f"建议：{random.choice(['适合户外活动', '记得带伞', '注意防晒', '适当添衣'])}。"
            )

        # 默认回复
        return (
            f"你提到了关于「{user_content[:50]}」的问题。\n\n"
            f"作为{character_name}，我来为你详细解答：\n\n"
            f"这个问题可以从以下几个方面来理解：\n\n"
            f"1. **背景分析** — 首先需要了解问题的上下文和具体需求\n"
            f"2. **核心要点** — 问题的关键点在于找到合适的解决方法\n"
            f"3. **实践建议** — 建议从简单场景开始，逐步扩展到复杂情况\n\n"
            f"如果你能提供更多细节，我可以给出更精准的回答。有其他问题随时告诉我！"
        )

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """粗略估算 token 数（中文约 1.5 字符/token，英文约 4 字符/token）"""
        chinese_chars = sum(1 for c in text if '一' <= c <= '鿿')
        other_chars = len(text) - chinese_chars
        return int(chinese_chars / 1.5 + other_chars / 4) + 1
