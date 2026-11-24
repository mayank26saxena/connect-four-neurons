#!/bin/zsh
# usage: a.sh seq1 seq2 ... ; prints final activation of U19
cd {REPO}
for s in "$@"; do
  v=$(uv run python scripts/31_ns_tool.py act U19 --moves $s 2>&1 | grep "after" | tail -1 | sed 's/.*: //')
  echo "$s => $v"
done
