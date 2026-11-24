#!/bin/zsh
# usage: t.sh "spec" ...   prints activation of final position
cd {REPO}
export C4N_CONFIG=ns2 NS_DIR={REPO}/ns2
for s in "$@"; do
  m=$(python3 -I ns2/work/U29/mk.py "$s")
  if [[ $m == IMPOSSIBLE ]]; then echo "$s  IMPOSSIBLE"; continue; fi
  a=$(uv run python scripts/31_ns_tool.py act U29 --moves $m | grep "after" | tail -1 | sed 's/.*): //')
  echo "$s  -> $a   [$m]"
done
