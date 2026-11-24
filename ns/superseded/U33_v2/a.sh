#!/bin/zsh
cd {REPO}
for m in "$@"; do
  echo -n "$m => "; uv run python scripts/31_ns_tool.py act U33 --moves $m 2>&1 | grep "after" | tail -1 | sed 's/.*: //'
done
