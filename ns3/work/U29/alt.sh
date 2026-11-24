#!/bin/bash
# usage: alt.sh moves(with last removed)
base=$1
for c in 0 1 2 3 4 5 6; do
  r=$(uv run python scripts/31_ns_tool.py act U29 --moves $base,$c 2>&1 | grep -E "after +[0-9]+ moves \($base,$c\)" | sed 's/.*://')
  echo "$c: $r"
done
