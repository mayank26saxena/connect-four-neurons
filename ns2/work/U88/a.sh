#!/bin/bash
# usage: a.sh seq1 seq2 ... ; prints final activation per sequence
cd {REPO}
export C4N_CONFIG=ns2 NS_DIR={REPO}/ns2
for s in "$@"; do
  n=$(echo "$s" | tr ',' '\n' | wc -l | tr -d ' ')
  v=$(uv run python scripts/31_ns_tool.py act U88 --moves "$s" 2>&1 | grep "after *$n moves" | sed -E 's/.*\): (-?[0-9.]+).*/\1/')
  echo "$s $v"
done
