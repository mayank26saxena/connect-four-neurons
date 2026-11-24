#!/bin/zsh
# usage: a.sh seq1 seq2 ... prints final activation for each
cd {REPO}
export C4N_CONFIG=ns2 NS_DIR={REPO}/ns2
for s in "$@"; do
  v=$(uv run python scripts/31_ns_tool.py act U79 --moves $s 2>&1 | grep "after" | tail -1 | sed 's/.*): //')
  echo "$s => $v"
done
