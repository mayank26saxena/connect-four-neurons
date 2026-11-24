#!/bin/zsh
# usage: a.sh seq...  prints final activation per sequence
cd {REPO}
export C4N_CONFIG=ns2 NS_DIR={REPO}/ns2
for s in "$@"; do
  v=$(uv run python scripts/31_ns_tool.py act U48 --moves $s 2>&1 | grep "after" | tail -${K:-1} | sed -E 's/.*\): //' | tr '\n' ' ')
  echo "$s => $v"
done
