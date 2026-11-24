#!/bin/bash
# usage: acts.sh seq1 seq2 ... ; prints final activation for each
cd {REPO}
for m in "$@"; do
  v=$(uv run python scripts/31_ns_tool.py act U02 --moves $m 2>&1 | grep "after " | tail -1 | sed -E 's/.*\): (-?[0-9.]+).*/\1/')
  echo "$m $v"
done
