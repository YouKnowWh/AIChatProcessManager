#!/bin/zsh

set -euo pipefail

cd /Users/alex/Projects/AIChatProcessManager

printf '\e[3J\e[H\e[2J'
printf 'AIChatProcessManager :: real message flow\n'
printf 'waiting for backend logs...\n\n'

docker compose logs -f backend --tail 0 \
  | rg --line-buffered 'message_flow|POST /api/auth/login|POST /api/conversations/1/messages' \
  | awk 'NR<=14 { print; fflush() } NR==14 { exit }'
