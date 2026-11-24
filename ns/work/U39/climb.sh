#!/bin/zsh
cd {REPO}
cur=$1; rounds=$2
best=$(uv run python scripts/31_ns_tool.py act U39 --moves $cur 2>&1 | grep after | tail -1 | sed -E 's/.*\): (-?[0-9.]+).*/\1/')
for r in $(seq 1 $rounds); do
  IFS=, read -rA arr <<< "$cur"; n=${#arr[@]}; improved=0
  for i in $(seq 1 $n); do for c in 0 1 2 3 4 5 6; do
    [ $c -eq ${arr[$i]} ] && continue
    a=("${arr[@]}"); a[$i]=$c; s=$(IFS=,; echo "${a[*]}")
    v=$(uv run python scripts/31_ns_tool.py act U39 --moves $s 2>&1 | grep -E "after +$n moves" | sed -E 's/.*\): (-?[0-9.]+).*/\1/')
    [ -z "$v" ] && continue
    if (( v > best )); then best=$v; bs=$s; improved=1; fi
  done; done
  [ $improved -eq 0 ] && break
  cur=$bs; echo "round $r: $best $cur"
done
