#!/bin/bash
# usage: actv.sh seq1 seq2 ... ; prints final activation for each
cd {REPO}
export C4N_CONFIG=ns3 NS_DIR=$PWD/ns3
for s in "$@"; do
  v=$(uv run python scripts/31_ns_tool.py act U32 --moves $s 2>&1 | grep "after" | tail -1 | sed -E 's/.*\): (-?[0-9.]+).*/\1/')
  echo "$s $v"
done
