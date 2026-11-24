#!/bin/bash
# usage: ext.sh BASE  -> prints non-winning 2-move extensions with activation
P=$1; n=$(echo $P | tr ',' '\n' | wc -l); n=$((n+2))
for d in 0 1 2 3 4 5 6; do for e in 0 1 2 3 4 5 6; do
  w=$(uv run python ns/work/U40/checkwin.py $P,$d,$e 2>/dev/null | awk '{print $2}')
  [ "$w" != "None" ] && continue
  v=$(uv run python scripts/31_ns_tool.py act U40 --moves $P,$d,$e 2>&1 | grep "after *$n moves" | awk '{print $5}')
  [ -n "$v" ] && echo "$P,$d,$e $v"
done; done | sort -k2 -g -r | head -4
