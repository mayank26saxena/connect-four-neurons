#!/bin/bash
# usage: t.sh "board" ...
cd {REPO}
for b in "$@"; do m=$(python3 -I ns/work/U58/mk.py "$b"); a=$(uv run python scripts/31_ns_tool.py act U58 --moves $m 2>&1 | grep after | tail -1 | awk '{print $5,$6}'); echo "$b  [$m]  $a"; done
