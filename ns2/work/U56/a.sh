#!/bin/zsh
cd {REPO}
export C4N_CONFIG=ns2 NS_DIR={REPO}/ns2
for m in "$@"; do
  v=$(uv run python scripts/31_ns_tool.py act U56 --moves $m 2>&1 | grep "after" | tail -1 | sed 's/.*: //')
  echo "$m => $v"
done
