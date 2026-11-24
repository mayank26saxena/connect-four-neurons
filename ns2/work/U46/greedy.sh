#!/bin/bash
B=($1); N=${#B[@]}
for ((i=0;i<N;i++)); do for c in 0 1 2 3 4 5 6; do
 [ "${B[$i]}" = "$c" ] && continue
 M=("${B[@]}"); M[$i]=$c; S=$(IFS=,; echo "${M[*]}")
 r=$(uv run python scripts/31_ns_tool.py synth U46 --moves $S 2>&1 | head -1)
 case "$r" in *"pole activation 0.009"*|*"pole activation 0.01"*|*beat*|*above*) echo "$S $r";; esac
done; done
