#!/bin/bash
# usage: a.sh moves...  -> prints final activation for each move list
cd {REPO}
export C4N_CONFIG=ns3 NS_DIR={REPO}/ns3
for m in "$@"; do
  v=$(uv run python scripts/31_ns_tool.py act U22 --moves $m 2>&1 | grep "after" | tail -1 | sed 's/.*): //')
  echo "$m => $v"
done
