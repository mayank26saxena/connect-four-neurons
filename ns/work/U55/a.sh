#!/bin/bash
cd {REPO}
for m in "$@"; do
  v=$(uv run python scripts/31_ns_tool.py act U55 --moves $m 2>&1 | grep "after" | tail -1 | sed 's/.*: //')
  echo "$m => $v"
done
