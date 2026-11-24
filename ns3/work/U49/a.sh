#!/bin/bash
# usage: a.sh moves  -> prints final activation
cd {REPO}
export C4N_CONFIG=ns3 NS_DIR={REPO}/ns3
uv run python scripts/31_ns_tool.py act U49 --moves $1 2>&1 | grep "after" | tail -1 | sed -E 's/.*\): (-?[0-9.]+).*/\1/'
