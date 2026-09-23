#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
preview_url="${1:-http://127.0.0.1:4173}"
session="portfolio-diagram-export-$$"
trap 'agent-browser --session "$session" close >/dev/null 2>&1 || true' EXIT

agent-browser --session "$session" set viewport 1000 800 2
for name in poudy-infrastructure ingredient-review concurrent-likes database-consistency rag-pipeline; do
  agent-browser --session "$session" open "$preview_url/assets/diagrams/$name.svg"
  agent-browser --session "$session" eval 'document.fonts.ready.then(() => true)'
  agent-browser --session "$session" screenshot svg "$repo_dir/assets/diagrams/$name.png"
done
