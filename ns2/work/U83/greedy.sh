#!/bin/bash
cd {REPO}
export C4N_CONFIG=ns2 NS_DIR={REPO}/ns2
for seed in 4,0,3,0,5,3,5,4,4,5,5 6,3,3,0,5,5,5,5 5,5,5,3,3,0; do
  best=$seed
  for step in 1 2; do
    bv=-99; bs=""
    for x in 0 1 2 4 5 6; do for y in 0 1 2 4 5 6; do
      s="$best,$x,$y"
      v=$(uv run python scripts/31_ns_tool.py act U83 --moves $s 2>&1 | grep 'after' | tail -1 | awk '{print $5}')
      if [ -n "$v" ] && awk "BEGIN{exit !($v > $bv)}"; then bv=$v; bs=$s; fi
    done; done
    echo "seed $seed step $step best $bs $bv"
    best=$bs
  done
done
