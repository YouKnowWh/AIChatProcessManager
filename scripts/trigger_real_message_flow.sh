#!/bin/zsh

set -euo pipefail

TOKEN=$(
  curl -sS -X POST http://127.0.0.1:8000/api/auth/login \
    -H 'Content-Type: application/json' \
    -d '{"username":"user1","password":"user123"}' \
  | sed -n 's/.*"access_token":"\([^"]*\)".*/\1/p'
)

curl -sS -X POST http://127.0.0.1:8000/api/conversations/1/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"content":"请帮我搜索一下最近消息的处理流程，并说明 context、tool call、tool result、metadata 分别写入哪些表"}' \
  >/dev/null
