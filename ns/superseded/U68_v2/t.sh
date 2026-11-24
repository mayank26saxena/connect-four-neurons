#!/bin/bash
cd {REPO}
while read -r line; do
  [ -z "$line" ] && continue
  m=$(python3 ns/work/U68/build.py $line)
  if [ "$m" = "none" ] || [[ "$m" == bad* ]]; then echo "$line => $m"; continue; fi
  a=$(uv run python scripts/31_ns_tool.py act U68 --moves $m 2>&1 | grep -E "after +[0-9]+ moves" | tail -1 | awk '{print $NF, $(NF-1)}')
  echo "$line => $a   [$m]"
done
