#!/bin/zsh
# usage: lastact.sh moves  -> prints activation after the final move
cd {REPO}
uv run python scripts/31_ns_tool.py act U63 --moves "$1" 2>&1 | grep "after" | tail -1 | sed -E 's/.*\): (-?[0-9.]+).*/\1/'
