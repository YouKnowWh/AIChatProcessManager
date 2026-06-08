-- ============================================================
-- AIChatProcessManager — 数据库建表脚本
-- 版本: 1.0
-- 引擎: InnoDB, 字符集: utf8mb4
-- ============================================================

CREATE DATABASE IF NOT EXISTS aichat_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE aichat_db;

-- ============================================================
-- 1. users — 用户表
-- ============================================================
CREATE TABLE users (
    id          INT             NOT NULL AUTO_INCREMENT,
    username    VARCHAR(50)     NOT NULL,
    email       VARCHAR(100)    NOT NULL,
    password_hash VARCHAR(255)  NOT NULL,
    nickname    VARCHAR(50)     NULL,
    avatar      VARCHAR(500)    NULL,
    phone       VARCHAR(20)     NULL,
    bio         TEXT            NULL,
    role        ENUM('user','character_manager','admin') NOT NULL DEFAULT 'user',
    status      ENUM('active','disabled')                NOT NULL DEFAULT 'active',
    last_login_at DATETIME      NULL,
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_username (username),
    UNIQUE KEY uk_email (email),
    INDEX idx_role (role),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 2. ai_characters — AI 角色表
-- ============================================================
CREATE TABLE ai_characters (
    id            INT           NOT NULL AUTO_INCREMENT,
    creator_id    INT           NOT NULL,
    name          VARCHAR(100)  NOT NULL,
    avatar        VARCHAR(500)  NULL,
    description   TEXT          NULL,
    system_prompt TEXT          NULL,
    category      VARCHAR(50)   NULL,
    tags          VARCHAR(255)  NULL,
    status        ENUM('active','disabled') NOT NULL DEFAULT 'active',
    usage_count   INT           NOT NULL DEFAULT 0,
    created_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_name (name),
    INDEX idx_creator (creator_id),
    INDEX idx_status (status),
    INDEX idx_category (category),
    CONSTRAINT fk_character_creator FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 3. conversations — 会话表
-- ============================================================
CREATE TABLE conversations (
    id              INT         NOT NULL AUTO_INCREMENT,
    user_id         INT         NOT NULL,
    character_id    INT         NOT NULL,
    title           VARCHAR(200) NULL,
    status          ENUM('active','archived','deleted') NOT NULL DEFAULT 'active',
    last_message_at DATETIME    NULL,
    created_at      DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_user (user_id),
    INDEX idx_character (character_id),
    INDEX idx_status (status),
    INDEX idx_user_character (user_id, character_id),
    CONSTRAINT fk_conv_user      FOREIGN KEY (user_id)      REFERENCES users(id)         ON DELETE CASCADE,
    CONSTRAINT fk_conv_character FOREIGN KEY (character_id) REFERENCES ai_characters(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 4. messages — 消息主表
-- ============================================================
CREATE TABLE messages (
    id                INT         NOT NULL AUTO_INCREMENT,
    conversation_id   INT         NOT NULL,
    parent_message_id INT         NULL,
    sender_type       ENUM('user','ai','system','tool')    NOT NULL,
    role              ENUM('user','assistant','system','tool') NOT NULL,
    status            ENUM('normal','hidden','deleted')    NOT NULL DEFAULT 'normal',
    sequence_number   INT         NOT NULL DEFAULT 0,
    created_at        DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_conversation (conversation_id),
    INDEX idx_parent (parent_message_id),
    INDEX idx_sender_type (sender_type),
    INDEX idx_status (status),
    INDEX idx_conv_seq (conversation_id, sequence_number),
    CONSTRAINT fk_msg_conversation FOREIGN KEY (conversation_id)   REFERENCES conversations(id) ON DELETE CASCADE,
    CONSTRAINT fk_msg_parent      FOREIGN KEY (parent_message_id) REFERENCES messages(id)       ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 5. message_contents — 消息正文表
-- ============================================================
CREATE TABLE message_contents (
    id           INT          NOT NULL AUTO_INCREMENT,
    message_id   INT          NOT NULL,
    content_type ENUM('text','markdown','code','link','image') NOT NULL DEFAULT 'text',
    content      TEXT         NOT NULL,
    sort_order   INT          NOT NULL DEFAULT 0,
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_message (message_id),
    INDEX idx_message_order (message_id, sort_order),
    CONSTRAINT fk_content_message FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 6. message_reasoning — 推理过程表
-- ============================================================
CREATE TABLE message_reasoning (
    id                INT       NOT NULL AUTO_INCREMENT,
    message_id        INT       NOT NULL,
    reasoning_content TEXT      NOT NULL,
    visibility        ENUM('hidden','owner_visible','admin_visible','debug_only') NOT NULL DEFAULT 'hidden',
    created_at        DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_message (message_id),
    INDEX idx_visibility (visibility),
    CONSTRAINT fk_reasoning_message FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 7. tool_calls — 工具调用表
-- ============================================================
CREATE TABLE tool_calls (
    id           INT           NOT NULL AUTO_INCREMENT,
    message_id   INT           NOT NULL,
    tool_name    VARCHAR(100)  NOT NULL,
    tool_type    ENUM('search','database','calculator','file','api','custom') NOT NULL DEFAULT 'custom',
    arguments    JSON          NOT NULL,
    call_id      VARCHAR(100)  NULL,
    status       ENUM('pending','success','failed','timeout') NOT NULL DEFAULT 'pending',
    called_at    DATETIME      NULL,
    completed_at DATETIME      NULL,
    PRIMARY KEY (id),
    INDEX idx_message (message_id),
    INDEX idx_tool_type (tool_type),
    INDEX idx_status (status),
    CONSTRAINT fk_toolcall_message FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 8. tool_results — 工具结果表
-- ============================================================
CREATE TABLE tool_results (
    id             INT       NOT NULL AUTO_INCREMENT,
    tool_call_id   INT       NOT NULL,
    result_content JSON      NOT NULL,
    is_error       BOOLEAN   NOT NULL DEFAULT FALSE,
    created_at     DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_tool_call (tool_call_id),
    CONSTRAINT fk_result_toolcall FOREIGN KEY (tool_call_id) REFERENCES tool_calls(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 9. message_metadata — 消息元数据表
-- ============================================================
CREATE TABLE message_metadata (
    id                INT            NOT NULL AUTO_INCREMENT,
    message_id        INT            NOT NULL,
    model_name        VARCHAR(100)   NULL,
    provider          VARCHAR(50)    NULL,
    prompt_tokens     INT            NULL,
    completion_tokens INT            NULL,
    total_tokens      INT            NULL,
    duration_ms       INT            NULL,
    finish_reason     ENUM('stop','length','tool_calls','content_filter','error') NULL,
    temperature       DECIMAL(3,2)   NULL,
    top_p             DECIMAL(3,2)   NULL,
    created_at        DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_message (message_id),
    INDEX idx_model (model_name),
    INDEX idx_provider (provider),
    CONSTRAINT fk_metadata_message FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 10. message_favorites — 收藏表
-- ============================================================
CREATE TABLE message_favorites (
    id         INT       NOT NULL AUTO_INCREMENT,
    user_id    INT       NOT NULL,
    message_id INT       NOT NULL,
    created_at DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_user_message (user_id, message_id),
    INDEX idx_user (user_id),
    INDEX idx_message (message_id),
    CONSTRAINT fk_fav_user    FOREIGN KEY (user_id)    REFERENCES users(id)    ON DELETE CASCADE,
    CONSTRAINT fk_fav_message FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 11. feedbacks — 反馈表
-- ============================================================
CREATE TABLE feedbacks (
    id            INT          NOT NULL AUTO_INCREMENT,
    user_id       INT          NOT NULL,
    message_id    INT          NOT NULL,
    character_id  INT          NOT NULL,
    feedback_type ENUM('like','dislike','text') NOT NULL,
    content       TEXT         NULL,
    tags          VARCHAR(255) NULL,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_user_msg_type (user_id, message_id, feedback_type),
    INDEX idx_message (message_id),
    INDEX idx_character (character_id),
    CONSTRAINT fk_fb_user      FOREIGN KEY (user_id)      REFERENCES users(id)         ON DELETE CASCADE,
    CONSTRAINT fk_fb_message   FOREIGN KEY (message_id)   REFERENCES messages(id)      ON DELETE CASCADE,
    CONSTRAINT fk_fb_character FOREIGN KEY (character_id) REFERENCES ai_characters(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 12. system_logs — 系统日志表
-- ============================================================
CREATE TABLE system_logs (
    id          INT          NOT NULL AUTO_INCREMENT,
    user_id     INT          NULL,
    action      VARCHAR(100) NOT NULL,
    target_type VARCHAR(50)  NULL,
    target_id   INT          NULL,
    detail      TEXT         NULL,
    ip_address  VARCHAR(45)  NULL,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_user (user_id),
    INDEX idx_action (action),
    INDEX idx_target (target_type, target_id),
    INDEX idx_created (created_at),
    CONSTRAINT fk_log_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 13. audit_records — 审核记录表
-- ============================================================
CREATE TABLE audit_records (
    id          INT         NOT NULL AUTO_INCREMENT,
    admin_id    INT         NOT NULL,
    target_type VARCHAR(50) NOT NULL,
    target_id   INT         NOT NULL,
    action      ENUM('approve','reject','flag','review') NOT NULL,
    comment     TEXT        NULL,
    created_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_admin (admin_id),
    INDEX idx_target (target_type, target_id),
    INDEX idx_action (action),
    CONSTRAINT fk_audit_admin FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
