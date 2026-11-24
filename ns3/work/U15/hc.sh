#!/bin/bash
base=(6 2 0 6 6 0 5 3 3 3 3 5 5 5 6 5 0 2 6)
for i in 0 1 2 6 7 8 9 10 11 12 13 15 16 17; do for c in 0 1 2 3 4 5; do
 s=("${base[@]}"); [ "${s[$i]}" = "$c" ] && continue; s[$i]=$c; m=$(IFS=,; echo "${s[*]}")
 v=$(uv run python scripts/31_ns_tool.py act U15 --moves $m 2>&1 | grep 'after 19' | sed -E 's/.*\): (-?[0-9.]+).*/\1/')
 echo "$v $m"
done; done
