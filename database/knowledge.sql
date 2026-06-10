-- ============================================================
-- 14. knowledge_entries — 知识库表（用户级别）
-- ============================================================
CREATE TABLE knowledge_entries (
    id           INT          NOT NULL AUTO_INCREMENT,
    user_id      INT          NOT NULL,
    title        VARCHAR(200) NOT NULL,
    content      TEXT         NOT NULL,
    content_type ENUM('text','markdown','file') NOT NULL DEFAULT 'text',
    source       VARCHAR(500) NULL,
    status       ENUM('active','disabled')      NOT NULL DEFAULT 'active',
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    CONSTRAINT fk_knowledge_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 种子数据
-- ============================================================
INSERT INTO knowledge_entries (id, user_id, title, content, content_type, source, status) VALUES
(1, 3, 'Python 基础语法', 'Python 是一种解释型、面向对象的高级编程语言。基本数据类型：int, float, str, bool, list, tuple, dict, set。控制流：if/elif/else, for, while。函数定义：def func_name(params):', 'markdown', 'Python官方文档', 'active'),
(2, 3, '常见问题解答', 'Q: 如何安装 Python？A: python.org 下载或 brew install python3。Q: pip 慢？A: pip install -i https://pypi.tuna.tsinghua.edu.cn/simple 包名', 'markdown', NULL, 'active'),
(3, 4, '翻译规范说明', '中译英注意：保持原文语气，专业术语统一，避免中式英语。英译中注意：符合汉语表达习惯，长句拆分', 'text', NULL, 'active');
