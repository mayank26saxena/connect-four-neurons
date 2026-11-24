#!/bin/bash
# usage: run.sh "<board>" [last]
cd {REPO}
S=$(python3 ns3/work/U48/b2s.py "$1" $2)
if [ "$S" = NONE ]; then echo "$1 NONE"; exit; fi
V=$(C4N_CONFIG=ns3 NS_DIR=$PWD/ns3 uv run python scripts/31_ns_tool.py act U48 --moves $S 2>&1 | grep '^  after' | tail -1 | grep -oE ': -?[0-9.]+' | tr -d ': ')
echo "$1 last=$2 -> $V"
