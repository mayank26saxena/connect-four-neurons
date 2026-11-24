#!/bin/zsh
cd {REPO}
for s in "$@"; do
  v=$(uv run python scripts/31_ns_tool.py act U45 --moves $s 2>&1 | grep "after" | tail -1 | sed -E 's/.*\): //')
  echo "$s : $v"
done
