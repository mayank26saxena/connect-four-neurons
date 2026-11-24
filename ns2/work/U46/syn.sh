#!/bin/bash
B=(3 4 3 3 3 2 6 2 2 0 1 3 0 1 6 4 2 4 4 6 4 5 2 2 3 0 4)
for i in 1 3 5 7 9 11 13 15 17 19 21 23 25; do for j in 1 3 5 7 9 11 13 15 17 19 21 23 25; do
 [ $j -le $i ] && continue
 for ci in 5 6; do for cj in 5 6; do
 M=("${B[@]}"); M[$i]=$ci; M[$j]=$cj; S=$(IFS=,; echo "${M[*]}")
 r=$(uv run python scripts/31_ns_tool.py synth U46 --moves $S 2>&1 | head -1)
 case "$r" in *"does not count"*|*rror*|*llegal*) ;; *) echo "$S $r";; esac
 done; done; done; done
