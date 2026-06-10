#!/bin/zsh

set -euo pipefail

printf '\e[3J\e[H\e[2J'
printf '\e[?25l'
trap 'printf "\e[?25h\n"' EXIT

slow() {
  local text="$1"
  local delay="${2:-0.24}"
  printf "%s\n" "$text"
  sleep "$delay"
}

section() {
  printf "\n"
  slow "$1" "${2:-0.18}"
}

slow "AIChatProcessManager :: message ingestion trace" 0.2
slow "request -> context rebuild -> block split -> table writes -> commit" 0.2
slow "trace_id=7fd2a1c4  conversation_id=12  actor=user#3  character=Code Expert" 0.25
printf "\n"

section "[01] POST /api/conversations/12/messages"
slow "payload.content = \"Please check recent tool outputs and summarize them\""
slow "payload.intent  = \"trigger tool path + persist full trace\""

section "[02] rebuild context from history"
slow "SELECT * FROM conversations WHERE id = 12;"
slow "SELECT * FROM messages WHERE conversation_id = 12 ORDER BY sequence_number ASC;"
slow "SELECT * FROM message_contents WHERE message_id IN (<history_ids>) ORDER BY sort_order ASC;"
slow "[context] source tables => conversations + messages + message_contents"
slow "[context] no dedicated context table; history is rebuilt from prior rows"

section "[03] write user message row"
slow "INSERT INTO messages"
slow "  (id, conversation_id, sender_type, role, sequence_number)"
slow "VALUES"
slow "  (301, 12, 'user', 'user', 17)"
slow "[ok] user envelope persisted -> table: messages"

section "[04] write user content block"
slow "INSERT INTO message_contents"
slow "  (message_id, content_type, content, sort_order)"
slow "VALUES"
slow "  (301, 'text', '<user prompt>', 0)"
slow "[ok] user text block persisted -> table: message_contents"

section "[05] write ai message row"
slow "INSERT INTO messages"
slow "  (id, conversation_id, parent_message_id, sender_type, role, sequence_number)"
slow "VALUES"
slow "  (302, 12, 301, 'ai', 'assistant', 18)"
slow "[ok] ai envelope persisted -> table: messages"

section "[06] write ai content block"
slow "INSERT INTO message_contents"
slow "  (message_id, content_type, content, sort_order)"
slow "VALUES"
slow "  (302, 'text', '<assistant reply>', 0)"
slow "[ok] ai reply block persisted -> table: message_contents"

section "[07] write reasoning block"
slow "INSERT INTO message_reasoning"
slow "  (message_id, reasoning_content, visibility)"
slow "VALUES"
slow "  (302, '<reasoning summary>', 'owner_visible')"
slow "[ok] chain-of-thought summary persisted -> table: message_reasoning"

section "[08] write tool call block"
slow "INSERT INTO tool_calls"
slow "  (message_id, tool_name, tool_type, arguments, call_id, status)"
slow "VALUES"
slow "  (302, 'query_database', 'database', '{...}', 'call_81', 'success')"
slow "[ok] tool invocation persisted -> table: tool_calls"

section "[09] write tool result block"
slow "INSERT INTO tool_results"
slow "  (tool_call_id, result_content, is_error)"
slow "VALUES"
slow "  (81, '{...}', false)"
slow "[ok] tool output persisted -> table: tool_results"

section "[10] write metadata block"
slow "INSERT INTO message_metadata"
slow "  (message_id, model_name, provider, total_tokens, duration_ms, finish_reason)"
slow "VALUES"
slow "  (302, 'deepseek-chat', 'deepseek', 947, 1280, 'stop')"
slow "[ok] inference stats persisted -> table: message_metadata"

section "[11] write system log row"
slow "INSERT INTO system_logs"
slow "  (action, user_id, target_type, target_id, detail)"
slow "VALUES"
slow "  ('send_message', 1, 'message', 301, '{\"ai_message_id\":302}')"
slow "INSERT INTO system_logs"
slow "  (action, user_id, target_type, target_id, detail)"
slow "VALUES"
slow "  ('message_flow_trace', 1, 'message', 302, '{\"steps\":[...]}')"
slow "[ok] audit and trace persisted -> table: system_logs"

section "[12] commit transaction"
slow "COMMIT"
slow "[done] transaction committed; admin trace view can now replay the same flow" 0.22
printf "\n"
slow "scroll check -> latest lines should remain centered in viewport" 0.18
slow "end of trace" 0.15
sleep 0.6
