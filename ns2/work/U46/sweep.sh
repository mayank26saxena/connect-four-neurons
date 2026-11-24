#!/bin/bash
# usage: sweep.sh "m1 m2 ..."  -> substitute each move, print activation at final ply
B=($1); N=${#B[@]}
for ((i=0;i<N;i++)); do echo -n "i=$i orig=${B[$i]}: "; for c in 0 1 2 3 4 5 6; do M=("${B[@]}"); M[$i]=$c; S=$(IFS=,; echo "${M[*]}"); r=$(uv run python scripts/31_ns_tool.py act U46 --moves $S 2>&1 | grep "after $N moves" | sed -E 's/.*\): (-?[0-9.]+).*/\1/'); echo -n "$c:${r:-x} "; done; echo; done
