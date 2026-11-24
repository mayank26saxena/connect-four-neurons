#!/bin/bash
# usage: feat.sh band seed n  -> per-position: act, ply, open, full, #mythreats, #theirthreats
uv run python scripts/31_ns_tool.py examples U02 --band $1 --n $3 --seed $2 2>&1 | grep "\[pos" | while read l; do
 a=$(echo "$l" | sed 's/.*pole act \([-0-9.]*\).*/\1/'); mv=$(echo "$l" | sed 's/.*moves: \([0-9,]*\).*/\1/')
 f=$(uv run python scripts/31_ns_tool.py facts --moves $mv 2>&1)
 mt=$(echo "$f" | grep "all my threat" | grep -o "(" | wc -l); tt=$(echo "$f" | grep "all their threat" | grep -o "(" | wc -l)
 lg=$(echo "$f" | grep -o "legal: \[.*\]")
 echo "$a ply=$(echo $mv | tr ',' '\n' | wc -l) my=$mt their=$tt $lg"
done
