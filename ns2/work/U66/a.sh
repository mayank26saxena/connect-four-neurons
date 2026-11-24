#!/bin/zsh
cd {REPO}
export C4N_CONFIG=ns2 NS_DIR={REPO}/ns2
for m in "$@"; do
  echo "$m => $(uv run python scripts/31_ns_tool.py act U66 --moves $m 2>&1 | grep -E '^  after' | sed -E 's/.*\): ([-0-9.]+).*/\1/' | tail -n +5 | tr '\n' ' ')"
done
