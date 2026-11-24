#!/bin/bash
# usage: edits.sh m1,m2,...  -> activation after changing one move's column
IFS=, read -ra base <<< "$1"; n=${#base[@]}
for ((i=0;i<n;i++)); do line="idx$i(${base[$i]}):"; for c in 0 1 2 3 4 5 6; do [ $c = ${base[$i]} ] && continue; m=("${base[@]}"); m[$i]=$c; s=$(IFS=,; echo "${m[*]}"); v=$(uv run python scripts/31_ns_tool.py act U10 --moves $s 2>&1 | grep "after *$n moves" | awk '{print $5}'); line="$line c$c=${v:-x}"; done; echo "$line"; done
