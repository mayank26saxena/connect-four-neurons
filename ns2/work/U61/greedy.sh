#!/bin/zsh
# greedy 2-ply extension search maximizing U61 activation
B=$1; steps=$2
A() { uv run python scripts/31_ns_tool.py act U61 --moves $1 2>&1 | grep -E "after +[0-9]+ moves \($1\)" | sed 's/.*: //' | cut -d' ' -f1; }
for s in $(seq $steps); do
  best=-99; bm=""
  for x in 0 1 2 3 4 5 6; do for y in 0 1 2 3 4 5 6; do
    v=$(A $B,$x,$y); [[ -z "$v" ]] && continue
    if (( v > best )); then best=$v; bm=$B,$x,$y; fi
  done; done
  B=$bm; echo "step $s: $B $best"
done
