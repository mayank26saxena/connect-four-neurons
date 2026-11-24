#!/bin/zsh
# rows a, cols c: sequence a,$1,c (O at a and c, X at $1)
cd {REPO}
x=$1
for a in 0 1 2 3 4 5 6; do line="$a:"; for c in 0 1 2 3 4 5 6; do s=$a,$x,$c; v=$(uv run python scripts/31_ns_tool.py act U19 --moves $s 2>&1 | grep after | tail -1 | sed 's/.*: //' | awk '{print $1}'); line="$line $v"; done; echo $line; done
