#!/bin/zsh
cd {REPO}
for m in "$@"; do printf "%-40s %s\n" "$m" "$(uv run python scripts/31_ns_tool.py act U35 --moves $m | grep "after" | tail -1 | sed 's/.*): //')"; done
