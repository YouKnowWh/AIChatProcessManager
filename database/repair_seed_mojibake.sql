-- ============================================================
-- 一次性修复：早期初始化时未设置 SET NAMES 导致的种子数据乱码
-- 仅用于已被错误连接字符集写入的本地测试数据。
-- ============================================================

USE aichat_db;

SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

UPDATE users
SET
    nickname = CONVERT(CAST(CONVERT(nickname USING latin1) AS BINARY) USING utf8mb4),
    bio = CONVERT(CAST(CONVERT(bio USING latin1) AS BINARY) USING utf8mb4)
WHERE id BETWEEN 1 AND 4;

UPDATE ai_characters
SET
    name = CONVERT(CAST(CONVERT(name USING latin1) AS BINARY) USING utf8mb4),
    description = CONVERT(CAST(CONVERT(description USING latin1) AS BINARY) USING utf8mb4),
    system_prompt = CONVERT(CAST(CONVERT(system_prompt USING latin1) AS BINARY) USING utf8mb4),
    category = CONVERT(CAST(CONVERT(category USING latin1) AS BINARY) USING utf8mb4),
    tags = CONVERT(CAST(CONVERT(tags USING latin1) AS BINARY) USING utf8mb4)
WHERE id BETWEEN 1 AND 4;

UPDATE conversations
SET title = CONVERT(CAST(CONVERT(title USING latin1) AS BINARY) USING utf8mb4)
WHERE id BETWEEN 1 AND 4;

UPDATE message_contents
SET content = CONVERT(CAST(CONVERT(content USING latin1) AS BINARY) USING utf8mb4)
WHERE id BETWEEN 1 AND 9;

UPDATE message_reasoning
SET reasoning_content = CONVERT(CAST(CONVERT(reasoning_content USING latin1) AS BINARY) USING utf8mb4)
WHERE id BETWEEN 1 AND 3;

UPDATE feedbacks
SET
    content = CASE
        WHEN content IS NULL THEN NULL
        ELSE CONVERT(CAST(CONVERT(content USING latin1) AS BINARY) USING utf8mb4)
    END,
    tags = CONVERT(CAST(CONVERT(tags USING latin1) AS BINARY) USING utf8mb4)
WHERE id BETWEEN 1 AND 3;

UPDATE system_logs
SET detail = CONVERT(CAST(CONVERT(detail USING latin1) AS BINARY) USING utf8mb4)
WHERE id BETWEEN 1 AND 8;

UPDATE audit_records
SET comment = CONVERT(CAST(CONVERT(comment USING latin1) AS BINARY) USING utf8mb4)
WHERE id BETWEEN 1 AND 2;
