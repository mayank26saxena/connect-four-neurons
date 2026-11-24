#!/bin/bash
# usage: a.sh moves...  -> prints final activation for each sequence
cd {REPO}
for s in "$@"; do echo "$s: $(uv run python scripts/31_ns_tool.py act U32 --moves $s 2>&1 | grep after | tail -1 | sed 's/.*)://')"; done
