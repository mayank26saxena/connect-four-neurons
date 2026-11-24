#!/bin/zsh
# usage: scan.sh m1,m2,...  ; replaces each move by each other column, prints final act
base=$1
IFS=, read -rA arr <<< "$base"
n=${#arr[@]}
for i in $(seq 1 $n); do
  line="idx$((i-1)) (${arr[$i]}):"
  for c in 0 1 2 3 4 5 6; do
    if [ $c -eq ${arr[$i]} ]; then line="$line   .  "; continue; fi
    a=("${arr[@]}"); a[$i]=$c
    s=$(IFS=,; echo "${a[*]}")
    v=$(uv run python scripts/31_ns_tool.py act U39 --moves $s 2>&1 | grep -E "after +$n moves" | sed -E 's/.*\): (-?[0-9.]+).*/\1/')
    [ -z "$v" ] && v="ill"
    line="$line $v"
  done
  echo $line
done
