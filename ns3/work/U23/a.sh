#!/bin/bash
# usage: a.sh moves...  prints final activation for each sequence
cd {REPO}
export C4N_CONFIG=ns3 NS_DIR={REPO}/ns3
for m in "$@"; do
  v=$(uv run python scripts/31_ns_tool.py act U23 --moves $m 2>&1 | grep "after" | tail -1 | sed -E 's/.*\): (-?[0-9.]+).*/\1/')
  echo "$m => $v"
done
