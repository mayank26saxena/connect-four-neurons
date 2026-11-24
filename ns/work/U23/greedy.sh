#!/bin/sh
# usage: greedy.sh BASE ; tries all 2-move extensions, prints top 5
cd {REPO}
B=$1
for a in 0 1 2 3 4 5 6; do for b in 0 1 2 3 4 5 6; do echo "$B,$a,$b"; done; done | xargs -P 8 -I{} sh -c 'uv run python scripts/31_ns_tool.py act U23 --moves {} 2>&1 | grep after | tail -1' | grep FIRES | sed -E 's/.*\((.*)\): ([0-9.]+) FIRES/\2 \1/' | sort -g -r | head -5
