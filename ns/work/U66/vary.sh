#!/bin/bash
# usage: vary.sh m1,m2,...  -> for each move index, substitute each column, print final activation
IFS=, read -ra base <<< "$1"
n=${#base[@]}
for ((i=0;i<n;i++)); do line="idx$i(${base[$i]}):"; for c in 0 1 2 3 4 5 6; do m=("${base[@]}"); m[$i]=$c; s=$(IFS=,; echo "${m[*]}"); v=$(uv run python scripts/31_ns_tool.py act U66 --moves $s 2>&1 | grep "after *$n moves" | awk '{print $5}'); line="$line $c:${v:-ill}"; done; echo "$line"; done
