-- ============================================================
-- 14. knowledge_entries — 知识库表
-- ============================================================
CREATE TABLE knowledge_entries (
    id           INT          NOT NULL AUTO_INCREMENT,
    character_id INT          NOT NULL,
    title        VARCHAR(200) NOT NULL,
    content      TEXT         NOT NULL,
    content_type ENUM('text','markdown','file') NOT NULL DEFAULT 'text',
    source       VARCHAR(500) NULL,
    status       ENUM('active','disabled')      NOT NULL DEFAULT 'active',
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_character (character_id),
    INDEX idx_status (status),
    CONSTRAINT fk_knowledge_character FOREIGN KEY (character_id) REFERENCES ai_characters(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
