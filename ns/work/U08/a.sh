#!/bin/zsh
# usage: a.sh moves [k]  -> last k activations
cd {REPO}
uv run python scripts/31_ns_tool.py act U08 --moves $1 2>&1 | grep 'after' | sed -E 's/.*\): (-?[0-9.]+).*/\1/' | tail -${2:-4} | tr '\n' ' '; echo
