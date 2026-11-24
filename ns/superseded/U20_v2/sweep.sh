#!/bin/zsh
# usage: sweep.sh BASE  -> grid of activation after BASE,a,b
cd {REPO}
B=$1
for a in 0 1 2 3 4 5 6; do
  line="X$a:"
  for b in 0 1 2 3 4 5 6; do
    v=$(uv run python scripts/31_ns_tool.py act U20 --moves $B,$a,$b 2>/dev/null | grep "^  after" | tail -1 | sed -E 's/.*\): *([-0-9.]+).*/\1/')
    line="$line $(printf '%6s' $v)"
  done
  echo $line
done
