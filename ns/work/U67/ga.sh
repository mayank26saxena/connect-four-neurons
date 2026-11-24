#!/bin/zsh
# usage: ga.sh "grid spec" ... prints activation for each
cd {REPO}
for s in "$@"; do
  m=$(python3 ns/work/U67/g2m.py "$s") || { echo "$s: $m"; continue; }
  a=$(uv run python scripts/31_ns_tool.py act U67 --moves $m | grep "after" | tail -1 | sed 's/.*)://')
  echo "$s  -> $a"
done
