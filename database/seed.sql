-- ============================================================
-- AIChatProcessManager — 测试数据脚本
-- 版本: 1.0
-- 密码明文（仅供测试）:
--   admin    / admin123
--   manager  / manager123
--   user1    / user123
--   user2    / user456
-- ============================================================

USE aichat_db;

-- ============================================================
-- 1. 用户数据 (4 条)
-- ============================================================
INSERT INTO users (username, email, password_hash, nickname, role, status, bio, last_login_at) VALUES
('admin',   'admin@test.com',   '$2b$12$154vT6oX9H1WWds.31L92e5xwEMKLvAtR6MrEiQkxwBDUF.TtjiP2', '系统管理员', 'admin',             'active', '系统管理员账户',           '2026-06-01 08:00:00'),
('manager', 'manager@test.com', '$2b$12$TnVMpPJ1aH6gBS78dz73ueY8KYXnVAY30up9i5HN9rgEIhIFzYLCC', '角色维护者', 'character_manager', 'active', '负责维护 AI 角色',          '2026-06-01 09:00:00'),
('user1',   'user1@test.com',   '$2b$12$yBCV8NRRbHXZUNykG2.LQuEFoMMzcHaWl3Nk2Z91vtRqutMI.745u', '测试用户一', 'user',              'active', '普通用户一号',               '2026-06-02 10:00:00'),
('user2',   'user2@test.com',   '$2b$12$EN2d44yzMeHbQQHLErpuIegnMgIW1dK0Fz1VI6LZkmHm7cvheKVI6', '测试用户二', 'user',              'active', '普通用户二号',               '2026-06-02 11:00:00');

-- ============================================================
-- 2. AI 角色数据 (4 条)
-- ============================================================
INSERT INTO ai_characters (id, creator_id, name, avatar, description, system_prompt, category, tags, status, usage_count) VALUES
(1, 2, '通用助手',   'https://api.dicebear.com/7.x/bottts/svg?seed=assistant', '一个通用的 AI 助手，可以回答各种问题。',     '你是一个乐于助人的 AI 助手，请用中文简洁回答用户的问题。',                     '通用', '聊天,问答,日常',       'active', 15),
(2, 2, '代码专家',   'https://api.dicebear.com/7.x/bottts/svg?seed=coder',     '擅长编程和代码审查的 AI 助手。',             '你是一个资深代码专家，精通多种编程语言。回答代码问题时请给出清晰解释和示例。',   '编程', '代码,调试,架构',       'active', 8),
(3, 2, '文档写手',   'https://api.dicebear.com/7.x/bottts/svg?seed=writer',    '帮助撰写技术文档和报告的 AI 助手。',         '你是一个技术文档撰写专家，擅长写清晰结构化的文档。请使用 Markdown 格式回复。', '写作', '文档,报告,Markdown',   'active', 5),
(4, 2, '翻译官',     'https://api.dicebear.com/7.x/bottts/svg?seed=translator', '支持中英日韩多语言互译。',                   '你是一个专业的翻译助手，支持中文、英文、日文、韩文之间的互译。',               '翻译', '翻译,多语言',           'disabled', 2);

-- ============================================================
-- 3. 会话数据 (4 条)
-- ============================================================
INSERT INTO conversations (id, user_id, character_id, title, status, last_message_at) VALUES
(1, 3, 1, '随便聊聊',      'active',   '2026-06-08 10:30:00'),
(2, 3, 2, 'Python 代码问题', 'active',  '2026-06-08 10:35:00'),
(3, 4, 1, '今天天气怎么样',  'active',  '2026-06-08 11:00:00'),
(4, 3, 3, '课程设计报告',    'archived', '2026-06-05 16:00:00');

-- ============================================================
-- 4. 消息数据 — 会话 1 (5 条消息)
-- ============================================================

-- 消息 1: 用户发送
INSERT INTO messages (id, conversation_id, parent_message_id, sender_type, role, status, sequence_number, created_at) VALUES
(1, 1, NULL, 'user', 'user', 'normal', 1, '2026-06-08 10:00:00');

INSERT INTO message_contents (message_id, content_type, content, sort_order) VALUES
(1, 'text', '你好，请问你能帮我做些什么？', 0);

-- 消息 2: AI 回复 (带完整过程数据)
INSERT INTO messages (id, conversation_id, parent_message_id, sender_type, role, status, sequence_number, created_at) VALUES
(2, 1, 1, 'ai', 'assistant', 'normal', 2, '2026-06-08 10:00:02');

INSERT INTO message_contents (message_id, content_type, content, sort_order) VALUES
(2, 'text', '你好！我是通用助手，可以帮你做很多事情：\n\n1. **回答问题** — 涵盖知识、常识、学习等\n2. **写作辅助** — 写文章、润色、翻译\n3. **代码帮助** — 写代码、调试、解释代码逻辑\n4. **数据分析** — 帮你整理和分析数据\n\n有什么想让我帮忙的吗？😊', 0);

INSERT INTO message_reasoning (message_id, reasoning_content, visibility) VALUES
(2, '用户是初次打招呼，我应该友好地回复并介绍自己的能力范围。考虑到用户可能想快速了解我能做什么，采用列表形式清晰列出能力项，并在结尾用友好的语气引导继续对话。使用了一些 Markdown 格式让回复更易读，表情符号可以增加亲和力。', 'owner_visible');

INSERT INTO tool_calls (id, message_id, tool_name, tool_type, arguments, call_id, status, called_at, completed_at) VALUES
(1, 2, 'get_user_profile', 'database', '{"user_id": 3, "fields": ["username", "preferences", "history"]}', 'call_abc_001', 'success', '2026-06-08 10:00:01', '2026-06-08 10:00:01');

INSERT INTO tool_results (tool_call_id, result_content, is_error) VALUES
(1, '{"username": "user1", "preferences": {"language": "zh", "detail_level": "concise"}, "conversation_count": 3}', FALSE);

INSERT INTO message_metadata (message_id, model_name, provider, prompt_tokens, completion_tokens, total_tokens, duration_ms, finish_reason, temperature, top_p) VALUES
(2, 'claude-sonnet-4-6', 'anthropic', 156, 89, 245, 1230, 'stop', 0.70, 0.90);

-- 消息 3: 用户追问
INSERT INTO messages (id, conversation_id, parent_message_id, sender_type, role, status, sequence_number, created_at) VALUES
(3, 1, 2, 'user', 'user', 'normal', 3, '2026-06-08 10:15:00');

INSERT INTO message_contents (message_id, content_type, content, sort_order) VALUES
(3, 'text', '帮我写一个 Python 排序函数吧', 0);

-- 消息 4: AI 回复 (带工具调用链)
INSERT INTO messages (id, conversation_id, parent_message_id, sender_type, role, status, sequence_number, created_at) VALUES
(4, 1, 3, 'ai', 'assistant', 'normal', 4, '2026-06-08 10:15:03');

INSERT INTO message_contents (message_id, content_type, content, sort_order) VALUES
(4, 'text', '好的，这里是一个通用的 Python 排序函数：\n\n```python\ndef bubble_sort(arr: list) -> list:\n    """冒泡排序实现"""\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr\n\n# 示例\nnums = [64, 34, 25, 12, 22, 11, 90]\nprint(bubble_sort(nums))  # [11, 12, 22, 25, 34, 64, 90]\n```\n\n这是冒泡排序，时间复杂度 O(n²)。需要其他排序算法（快排、归并）的话告诉我。', 0);

INSERT INTO message_contents (message_id, content_type, content, sort_order) VALUES
(4, 'code', 'def bubble_sort(arr: list) -> list:\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr', 1);

INSERT INTO message_reasoning (message_id, reasoning_content, visibility) VALUES
(4, '用户想写一个排序函数，但没有指定具体排序算法和语言（虽然上下文是 Python 对话）。按照"简洁回答"偏好，选择一个最易理解的冒泡排序作为示例。同时提供代码与解释分离的内容块。在代码块中使用 Markdown 语法高亮。备份代码块用纯文本便于复制。', 'owner_visible');

INSERT INTO tool_calls (id, message_id, tool_name, tool_type, arguments, call_id, status, called_at, completed_at) VALUES
(2, 4, 'search_sorting_examples', 'search', '{"query": "python bubble sort simple example", "limit": 3}', 'call_abc_002', 'success', '2026-06-08 10:15:01', '2026-06-08 10:15:02'),
(3, 4, 'validate_code', 'api', '{"code": "def bubble_sort(arr): ...", "language": "python", "check": ["syntax", "logic"]}', 'call_abc_003', 'success', '2026-06-08 10:15:02', '2026-06-08 10:15:03');

INSERT INTO tool_results (tool_call_id, result_content, is_error) VALUES
(2, '{"found": 3, "examples": [{"title": "Bubble Sort in Python", "url": "https://example.com/1"}, {"title": "Sorting Algorithms Compared", "url": "https://example.com/2"}]}', FALSE),
(3, '{"valid": true, "issues": [], "complexity": "O(n^2)", "suggestions": ["Consider using built-in sorted() for production"]}', FALSE);

INSERT INTO message_metadata (message_id, model_name, provider, prompt_tokens, completion_tokens, total_tokens, duration_ms, finish_reason, temperature, top_p) VALUES
(4, 'claude-sonnet-4-6', 'anthropic', 312, 178, 490, 2450, 'stop', 0.70, 0.90);

-- 消息 5: 用户感谢
INSERT INTO messages (id, conversation_id, parent_message_id, sender_type, role, status, sequence_number, created_at) VALUES
(5, 1, 4, 'user', 'user', 'normal', 5, '2026-06-08 10:30:00');

INSERT INTO message_contents (message_id, content_type, content, sort_order) VALUES
(5, 'text', '谢谢，解释得很清楚！', 0);

-- ============================================================
-- 5. 消息数据 — 会话 2 (2 条消息，简化)
-- ============================================================
INSERT INTO messages (id, conversation_id, parent_message_id, sender_type, role, status, sequence_number, created_at) VALUES
(6, 2, NULL, 'user', 'user', 'normal', 1, '2026-06-08 10:30:00');

INSERT INTO message_contents (message_id, content_type, content, sort_order) VALUES
(6, 'text', 'Python 中如何处理 CSV 文件？', 0);

INSERT INTO messages (id, conversation_id, parent_message_id, sender_type, role, status, sequence_number, created_at) VALUES
(7, 2, 6, 'ai', 'assistant', 'normal', 2, '2026-06-08 10:30:03');

INSERT INTO message_contents (message_id, content_type, content, sort_order) VALUES
(7, 'text', 'Python 处理 CSV 文件最常见的方式是用 `csv` 标准库或 `pandas`：\n\n```python\nimport csv\n\n# 读取 CSV\nwith open(""data.csv"", ""r"") as f:\n    reader = csv.DictReader(f)\n    for row in reader:\n        print(row)\n\n# 写入 CSV\nwith open(""output.csv"", ""w"") as f:\n    writer = csv.DictWriter(f, fieldnames=[""name"", ""age""])\n    writer.writeheader()\n    writer.writerow({""name"": ""张三"", ""age"": 25})\n```\n\n数据量大推荐 `pandas.read_csv()`，小文件用标准库就够了。', 0);

INSERT INTO message_reasoning (message_id, reasoning_content, visibility) VALUES
(7, '用户问 CSV 处理。这是 Python 常见需求，不需要搜索外部资料。给两种主流方案：标准库 csv（无需安装依赖）和 pandas（功能更强）。按"简洁"偏好，重点展示标准库方案，提到 pandas 作为备选。代码包含读和写两个方向的实例。', 'owner_visible');

INSERT INTO message_metadata (message_id, model_name, provider, prompt_tokens, completion_tokens, total_tokens, duration_ms, finish_reason, temperature, top_p) VALUES
(7, 'claude-sonnet-4-6', 'anthropic', 201, 132, 333, 1890, 'stop', 0.70, 0.90);

-- ============================================================
-- 6. 消息数据 — 会话 3 (1 条用户消息，模拟被隐藏)
-- ============================================================
INSERT INTO messages (id, conversation_id, parent_message_id, sender_type, role, status, sequence_number, created_at) VALUES
(8, 3, NULL, 'user', 'user', 'hidden', 1, '2026-06-08 11:00:00');

INSERT INTO message_contents (message_id, content_type, content, sort_order) VALUES
(8, 'text', '这条消息包含不当内容，已被管理员隐藏。', 0);

-- ============================================================
-- 7. 收藏数据 (user1 收藏了 2 条 AI 消息)
-- ============================================================
INSERT INTO message_favorites (user_id, message_id, created_at) VALUES
(3, 2, '2026-06-08 10:05:00'),
(3, 4, '2026-06-08 10:20:00');

-- ============================================================
-- 8. 反馈数据
-- ============================================================
INSERT INTO feedbacks (user_id, message_id, character_id, feedback_type, content, tags, created_at) VALUES
(3, 2, 1, 'like', NULL, '友好,有帮助', '2026-06-08 10:05:00'),
(3, 4, 1, 'like', NULL, '代码清晰', '2026-06-08 10:20:00'),
(4, 7, 2, 'text', '希望增加 JSON 处理的示例。', '建议,数据', '2026-06-08 10:35:00');

-- ============================================================
-- 9. 系统日志数据
-- ============================================================
INSERT INTO system_logs (user_id, action, target_type, target_id, detail, ip_address, created_at) VALUES
(1, 'login',        NULL,     NULL, '{"result": "success"}',                                       '127.0.0.1', '2026-06-01 08:00:00'),
(3, 'login',        NULL,     NULL, '{"result": "success"}',                                       '127.0.0.1', '2026-06-01 09:00:00'),
(3, 'create_conversation', 'conversation', 1, '{"character_id": 1, "title": "随便聊聊"}',         '127.0.0.1', '2026-06-08 10:00:00'),
(3, 'send_message', 'message', 1, '{"conversation_id": 1, "sender_type": "user"}',                '127.0.0.1', '2026-06-08 10:00:00'),
(3, 'send_message', 'message', 3, '{"conversation_id": 1, "sender_type": "user"}',                '127.0.0.1', '2026-06-08 10:15:00'),
(4, 'login',        NULL,     NULL, '{"result": "success"}',                                       '127.0.0.1', '2026-06-08 11:00:00'),
(4, 'send_message', 'message', 8, '{"sender_type": "user"}',                                       '127.0.0.1', '2026-06-08 11:00:00'),
(1, 'hide_message', 'message', 8, '{"reason": "violation of content policy", "admin_id": 1}',     '127.0.0.1', '2026-06-08 11:05:00');

-- ============================================================
-- 10. 审核记录数据
-- ============================================================
INSERT INTO audit_records (admin_id, target_type, target_id, action, comment, created_at) VALUES
(1, 'message', 8, 'flag', '用户举报该消息含不当内容，已隐藏处理。', '2026-06-08 11:05:00'),
(1, 'ai_character', 4, 'approve', '翻译官角色审核通过，目前处于禁用状态等待维护者启用。', '2026-06-05 14:00:00');
