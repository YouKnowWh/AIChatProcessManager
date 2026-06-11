-- ============================================================
-- 15. context_segments — 会话上下文片段
-- ============================================================
CREATE TABLE IF NOT EXISTS context_segments (
    id               INT          NOT NULL AUTO_INCREMENT,
    conversation_id  INT          NOT NULL,
    segment_type     ENUM('recent_messages','manual','system') NOT NULL DEFAULT 'recent_messages',
    summary_text     TEXT         NULL,
    start_message_id INT          NULL,
    end_message_id   INT          NULL,
    token_count      INT          NOT NULL DEFAULT 0,
    status           ENUM('active','archived') NOT NULL DEFAULT 'active',
    created_at       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_conversation (conversation_id),
    INDEX idx_status (status),
    CONSTRAINT fk_cs_conversation FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    CONSTRAINT fk_cs_start_msg FOREIGN KEY (start_message_id) REFERENCES messages(id) ON DELETE SET NULL,
    CONSTRAINT fk_cs_end_msg FOREIGN KEY (end_message_id) REFERENCES messages(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 16. message_context_refs — 消息与上下文片段的引用关系
-- ============================================================
CREATE TABLE IF NOT EXISTS message_context_refs (
    id                 INT          NOT NULL AUTO_INCREMENT,
    message_id         INT          NOT NULL,
    context_segment_id INT          NOT NULL,
    ref_type           ENUM('used','cited','generated') NOT NULL DEFAULT 'used',
    created_at         DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_message (message_id),
    INDEX idx_context (context_segment_id),
    UNIQUE KEY uk_msg_ctx_type (message_id, context_segment_id, ref_type),
    CONSTRAINT fk_mcr_message FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE,
    CONSTRAINT fk_mcr_context FOREIGN KEY (context_segment_id) REFERENCES context_segments(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
