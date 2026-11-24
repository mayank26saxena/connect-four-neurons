#!/bin/bash
uv run python scripts/31_ns_tool.py examples U02 --band $1 --n $3 --seed $2 2>&1 | grep "\[pos" | while read l; do
 a=$(echo "$l" | sed 's/.*pole act \([-0-9.]*\).*/\1/'); mv=$(echo "$l" | sed 's/.*moves: \([0-9,]*\).*/\1/')
 f=$(uv run python scripts/31_ns_tool.py facts --moves $mv 2>&1)
 echo "$a $(echo "$f" | grep -o 'me = [a-z]*') $(echo "$f" | grep teacher | sed 's/.*: //')"
done
