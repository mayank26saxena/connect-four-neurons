#!/bin/bash
# usage: t.sh movesA movesB ... ; prints final activation, board, threats
cd {REPO}
for m in "$@"; do
  echo "== $m"
  uv run python scripts/31_ns_tool.py act U21 --moves $m 2>&1 | grep "after" | tail -1
  uv run python scripts/31_ns_tool.py facts --moves $m 2>&1 | grep -E "^[.XO]{7}$|threat cells|landing rows"
done
