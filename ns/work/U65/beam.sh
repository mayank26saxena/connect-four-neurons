#!/bin/sh
# usage: beam.sh seeds_file out_file ; extends each seed by 2 plies, records final activation
cd {REPO}
while read s; do for x in 0 1 2 3 4 5 6; do for y in 0 1 2 3 4 5 6; do echo "$s,$x,$y"; done; done; done < "$1" | \
xargs -P 8 -I{} sh -c 'v=$(uv run python scripts/31_ns_tool.py act U65 --moves {} 2>&1 | grep "after" | tail -1 | awk "{print \$5}"); echo "$v {}"' > "$2"
