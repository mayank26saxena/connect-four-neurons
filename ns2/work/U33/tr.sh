#!/bin/bash
# print compact trace: lastcol:act for each prefix
cd {REPO}
uv run python scripts/31_ns_tool.py act U33 --moves "$1" 2>&1 | grep 'after' | sed -E 's/.*moves \(([0-9,]*)\): ([-0-9.]+).*/\1 \2/' | awk '{n=split($1,z,","); h=0; for(i=1;i<=n;i++) if(z[i]==z[n]) h++; printf "%s/%d:%s ", z[n], h-1, $2} END{print ""}'
