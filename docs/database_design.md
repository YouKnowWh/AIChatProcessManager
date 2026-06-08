# AIChatProcessManager 数据库设计文档

## 1. ER 图

```mermaid
erDiagram
    users ||--o{ ai_characters : "创建 (creator_id)"
    users ||--o{ conversations : "拥有 (user_id)"
    users ||--o{ feedbacks : "提交"
    users ||--o{ system_logs : "产生"
    users ||--o{ audit_records : "审核 (admin_id)"
    users ||--o{ message_favorites : "收藏"

    ai_characters ||--o{ conversations : "所属"
    ai_characters ||--o{ feedbacks : "收到反馈"

    conversations ||--o{ messages : "包含"

    messages ||--o{ message_contents : "正文内容"
    messages ||--o| message_reasoning : "推理过程"
    messages ||--o{ tool_calls : "工具调用"
    messages ||--o| message_metadata : "模型元数据"
    messages ||--o{ feedbacks : "收到反馈"
    messages ||--o{ message_favorites : "被收藏"

    tool_calls ||--o| tool_results : "调用结果"

    users {
        int id PK
        varchar username UK
        varchar email UK
        varchar password_hash
        varchar nickname
        varchar avatar
        varchar phone
        varchar bio
        enum role "user, character_manager, admin"
        enum status "active, disabled"
        datetime last_login_at
        datetime created_at
        datetime updated_at
    }

    ai_characters {
        int id PK
        int creator_id FK
        varchar name UK
        varchar avatar
        text description
        text system_prompt
        varchar category
        varchar tags
        enum status "active, disabled"
        int usage_count
        datetime created_at
        datetime updated_at
    }

    conversations {
        int id PK
        int user_id FK
        int character_id FK
        varchar title
        enum status "active, archived, deleted"
        datetime last_message_at
        datetime created_at
        datetime updated_at
    }

    messages {
        int id PK
        int conversation_id FK
        int parent_message_id FK_nullable
        enum sender_type "user, ai, system, tool"
        enum role "user, assistant, system, tool"
        enum status "normal, hidden, deleted"
        int sequence_number
        datetime created_at
    }

    message_contents {
        int id PK
        int message_id FK
        varchar content_type "text, markdown, code, link"
        text content
        int sort_order
        datetime created_at
    }

    message_reasoning {
        int id PK
        int message_id FK
        text reasoning_content
        enum visibility "hidden, owner_visible, admin_visible, debug_only"
        datetime created_at
    }

    tool_calls {
        int id PK
        int message_id FK
        varchar tool_name
        varchar tool_type "search, database, calculator, file, api, custom"
        json arguments
        varchar call_id
        enum status "pending, success, failed, timeout"
        datetime called_at
        datetime completed_at
    }

    tool_results {
        int id PK
        int tool_call_id FK
        json result_content
        boolean is_error
        datetime created_at
    }

    message_metadata {
        int id PK
        int message_id FK
        varchar model_name
        varchar provider
        int prompt_tokens
        int completion_tokens
        int total_tokens
        int duration_ms
        varchar finish_reason "stop, length, tool_calls, content_filter, error"
        decimal temperature
        decimal top_p
        datetime created_at
    }

    message_favorites {
        int id PK
        int user_id FK
        int message_id FK
        datetime created_at
    }

    feedbacks {
        int id PK
        int user_id FK
        int message_id FK
        int character_id FK
        enum feedback_type "like, dislike, text"
        text content
        text tags
        datetime created_at
    }

    system_logs {
        int id PK
        int user_id FK_nullable
        varchar action
        varchar target_type
        int target_id
        text detail
        varchar ip_address
        datetime created_at
    }

    audit_records {
        int id PK
        int admin_id FK
        varchar target_type
        int target_id
        enum action "approve, reject, flag, review"
        text comment
        datetime created_at
    }
```

## 2. 详细表结构

### 2.1 users — 用户表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 用户 ID |
| `username` | VARCHAR(50) | NOT NULL, UNIQUE | 用户名 |
| `email` | VARCHAR(100) | NOT NULL, UNIQUE | 邮箱 |
| `password_hash` | VARCHAR(255) | NOT NULL | bcrypt 密码哈希 |
| `nickname` | VARCHAR(50) | NULL | 昵称 |
| `avatar` | VARCHAR(500) | NULL | 头像 URL |
| `phone` | VARCHAR(20) | NULL | 手机号 |
| `bio` | TEXT | NULL | 个人简介 |
| `role` | ENUM('user','character_manager','admin') | NOT NULL, DEFAULT 'user' | 用户角色 |
| `status` | ENUM('active','disabled') | NOT NULL, DEFAULT 'active' | 账户状态 |
| `last_login_at` | DATETIME | NULL | 最后登录时间 |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

**索引：** UNIQUE(`username`), UNIQUE(`email`), INDEX(`role`), INDEX(`status`)

---

### 2.2 ai_characters — AI 角色表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 角色 ID |
| `creator_id` | INT | FK → users.id, NOT NULL | 创建者 |
| `name` | VARCHAR(100) | NOT NULL, UNIQUE | 角色名称 |
| `avatar` | VARCHAR(500) | NULL | 头像 URL |
| `description` | TEXT | NULL | 角色简介 |
| `system_prompt` | TEXT | NULL | 基础提示词 |
| `category` | VARCHAR(50) | NULL | 适用场景/分类 |
| `tags` | VARCHAR(255) | NULL | 标签（逗号分隔） |
| `status` | ENUM('active','disabled') | NOT NULL, DEFAULT 'active' | 角色状态 |
| `usage_count` | INT | NOT NULL, DEFAULT 0 | 使用次数 |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

**索引：** UNIQUE(`name`), INDEX(`creator_id`), INDEX(`status`), INDEX(`category`)

---

### 2.3 conversations — 会话表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 会话 ID |
| `user_id` | INT | FK → users.id, NOT NULL | 所属用户 |
| `character_id` | INT | FK → ai_characters.id, NOT NULL | 使用的 AI 角色 |
| `title` | VARCHAR(200) | NULL | 会话标题 |
| `status` | ENUM('active','archived','deleted') | NOT NULL, DEFAULT 'active' | 会话状态 |
| `last_message_at` | DATETIME | NULL | 最后一条消息时间 |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

**索引：** INDEX(`user_id`), INDEX(`character_id`), INDEX(`status`), INDEX(`user_id`, `character_id`)

---

### 2.4 messages — 消息主表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 消息 ID |
| `conversation_id` | INT | FK → conversations.id, NOT NULL | 所属会话 |
| `parent_message_id` | INT | FK → messages.id, NULL | 父消息（用户消息 → AI 回复） |
| `sender_type` | ENUM('user','ai','system','tool') | NOT NULL | 发送者类型 |
| `role` | ENUM('user','assistant','system','tool') | NOT NULL | 消息角色 |
| `status` | ENUM('normal','hidden','deleted') | NOT NULL, DEFAULT 'normal' | 消息状态 |
| `sequence_number` | INT | NOT NULL | 会话内消息序号 |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**索引：** INDEX(`conversation_id`), INDEX(`parent_message_id`), INDEX(`sender_type`), INDEX(`status`), INDEX(`conversation_id`, `sequence_number`)

---

### 2.5 message_contents — 消息正文表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 内容 ID |
| `message_id` | INT | FK → messages.id, NOT NULL | 所属消息 |
| `content_type` | ENUM('text','markdown','code','link','image') | NOT NULL, DEFAULT 'text' | 内容类型 |
| `content` | TEXT | NOT NULL | 正文内容 |
| `sort_order` | INT | NOT NULL, DEFAULT 0 | 排序（多段内容时） |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**索引：** INDEX(`message_id`), INDEX(`message_id`, `sort_order`)

---

### 2.6 message_reasoning — 推理过程表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 记录 ID |
| `message_id` | INT | FK → messages.id, NOT NULL, UNIQUE | 所属消息（1 对 1） |
| `reasoning_content` | TEXT | NOT NULL | 推理内容 |
| `visibility` | ENUM('hidden','owner_visible','admin_visible','debug_only') | NOT NULL, DEFAULT 'hidden' | 可见性控制 |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**索引：** UNIQUE(`message_id`), INDEX(`visibility`)

---

### 2.7 tool_calls — 工具调用表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 调用 ID |
| `message_id` | INT | FK → messages.id, NOT NULL | 所属 AI 消息 |
| `tool_name` | VARCHAR(100) | NOT NULL | 工具名称 |
| `tool_type` | ENUM('search','database','calculator','file','api','custom') | NOT NULL, DEFAULT 'custom' | 工具类型 |
| `arguments` | JSON | NOT NULL | 调用参数 |
| `call_id` | VARCHAR(100) | NULL | 调用唯一标识 |
| `status` | ENUM('pending','success','failed','timeout') | NOT NULL, DEFAULT 'pending' | 调用状态 |
| `called_at` | DATETIME | NULL | 调用时间 |
| `completed_at` | DATETIME | NULL | 完成时间 |

**索引：** INDEX(`message_id`), INDEX(`tool_type`), INDEX(`status`)

---

### 2.8 tool_results — 工具结果表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 结果 ID |
| `tool_call_id` | INT | FK → tool_calls.id, NOT NULL, UNIQUE | 所属工具调用（1 对 1） |
| `result_content` | JSON | NOT NULL | 返回结果 |
| `is_error` | BOOLEAN | NOT NULL, DEFAULT FALSE | 是否为错误结果 |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**索引：** UNIQUE(`tool_call_id`)

---

### 2.9 message_metadata — 消息元数据表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 元数据 ID |
| `message_id` | INT | FK → messages.id, NOT NULL, UNIQUE | 所属 AI 消息（1 对 1） |
| `model_name` | VARCHAR(100) | NULL | 模型名，如 gpt-4、claude-opus-4 |
| `provider` | VARCHAR(50) | NULL | 提供商，如 openai、anthropic |
| `prompt_tokens` | INT | NULL | 提示词 token 数 |
| `completion_tokens` | INT | NULL | 生成 token 数 |
| `total_tokens` | INT | NULL | 总 token 数 |
| `duration_ms` | INT | NULL | 耗时（毫秒） |
| `finish_reason` | ENUM('stop','length','tool_calls','content_filter','error') | NULL | 结束原因 |
| `temperature` | DECIMAL(3,2) | NULL | 温度参数 |
| `top_p` | DECIMAL(3,2) | NULL | Top-P 参数 |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**索引：** UNIQUE(`message_id`), INDEX(`model_name`), INDEX(`provider`)

---

### 2.10 message_favorites — 收藏表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 收藏 ID |
| `user_id` | INT | FK → users.id, NOT NULL | 用户 |
| `message_id` | INT | FK → messages.id, NOT NULL | 收藏的消息 |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 收藏时间 |

**索引：** UNIQUE(`user_id`, `message_id`), INDEX(`user_id`), INDEX(`message_id`)

---

### 2.11 feedbacks — 反馈表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 反馈 ID |
| `user_id` | INT | FK → users.id, NOT NULL | 反馈用户 |
| `message_id` | INT | FK → messages.id, NOT NULL | 被反馈的消息 |
| `character_id` | INT | FK → ai_characters.id, NOT NULL | 关联的 AI 角色 |
| `feedback_type` | ENUM('like','dislike','text') | NOT NULL | 反馈类型 |
| `content` | TEXT | NULL | 文字反馈内容 |
| `tags` | VARCHAR(255) | NULL | 反馈标签 |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 反馈时间 |

**索引：** UNIQUE(`user_id`, `message_id`, `feedback_type`)（同用户对同一消息同类型不重复）, INDEX(`message_id`), INDEX(`character_id`)

---

### 2.12 system_logs — 系统日志表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 日志 ID |
| `user_id` | INT | FK → users.id, NULL | 操作用户（未登录可为空） |
| `action` | VARCHAR(100) | NOT NULL | 操作名称，如 login、create_conversation |
| `target_type` | VARCHAR(50) | NULL | 操作对象类型 |
| `target_id` | INT | NULL | 操作对象 ID |
| `detail` | TEXT | NULL | 操作详情（JSON 字符串） |
| `ip_address` | VARCHAR(45) | NULL | IP 地址 |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 操作时间 |

**索引：** INDEX(`user_id`), INDEX(`action`), INDEX(`target_type`, `target_id`), INDEX(`created_at`)

---

### 2.13 audit_records — 审核记录表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INT | PK, AUTO_INCREMENT | 审核 ID |
| `admin_id` | INT | FK → users.id, NOT NULL | 审核管理员 |
| `target_type` | VARCHAR(50) | NOT NULL | 审核对象类型 |
| `target_id` | INT | NOT NULL | 审核对象 ID |
| `action` | ENUM('approve','reject','flag','review') | NOT NULL | 审核动作 |
| `comment` | TEXT | NULL | 审核意见 |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 审核时间 |

**索引：** INDEX(`admin_id`), INDEX(`target_type`, `target_id`), INDEX(`action`)

---

## 3. 关系汇总

| 关系 | 类型 | 外键 |
|------|------|------|
| user → ai_character | 1:N | `ai_characters.creator_id` → `users.id` |
| user → conversation | 1:N | `conversations.user_id` → `users.id` |
| ai_character → conversation | 1:N | `conversations.character_id` → `ai_characters.id` |
| conversation → message | 1:N | `messages.conversation_id` → `conversations.id` |
| message → message (parent) | 1:N (自引用) | `messages.parent_message_id` → `messages.id` |
| message → message_content | 1:N | `message_contents.message_id` → `messages.id` |
| message → message_reasoning | 1:1 | `message_reasoning.message_id` → `messages.id` |
| message → tool_call | 1:N | `tool_calls.message_id` → `messages.id` |
| tool_call → tool_result | 1:1 | `tool_results.tool_call_id` → `tool_calls.id` |
| message → message_metadata | 1:1 | `message_metadata.message_id` → `messages.id` |
| user → message (favorite) | N:M | `message_favorites.user_id` + `message_favorites.message_id` |
| user → feedback | 1:N | `feedbacks.user_id` → `users.id` |
| message → feedback | 1:N | `feedbacks.message_id` → `messages.id` |
| ai_character → feedback | 1:N | `feedbacks.character_id` → `ai_characters.id` |
| user → system_log | 1:N | `system_logs.user_id` → `users.id` |
| user (admin) → audit_record | 1:N | `audit_records.admin_id` → `users.id` |

## 4. 设计决策说明

1. **message 与子表拆分**：不把 content、reasoning、tool_calls、metadata 都塞进 messages，原因是：(a) 职责分离，查询普通消息时不加载大段推理文本；(b) 独立权限控制，reasoning 可见性可单独管理；(c) 扩展性好，后续加新类型不需改主表。

2. **tool_calls.tool_results 的关系**：第一阶段按 1 对 1 实现（`UNIQUE(tool_call_id)`），后续可扩展为一对多。

3. **message_reasoning 的 visibility 字段**：控制不同角色能否看到推理过程——普通聊天界面 `hidden`，消息拥有者可见 `owner_visible`，管理员可审查 `admin_visible`。

4. **软删除**：`conversations.status` 和 `messages.status` 用枚举标记状态，不做物理删除，方便管理员审查和数据恢复。

5. **JSON 字段**：`tool_calls.arguments` 和 `tool_results.result_content` 使用 JSON 类型，原生支持结构化查询，同时保留灵活性。
