#!/bin/bash
# simple hill-climb for synthesis: mutate one non-final move of the best sequence
cd {REPO}
export C4N_CONFIG=ns3 NS_DIR={REPO}/ns3
best="$1"; bestv=$(uv run python scripts/31_ns_tool.py synth U13 --moves $best 2>&1 | head -1 | sed -E 's/.*activation (-?[0-9.]+).*/\1/')
echo "start $best $bestv"
for it in $(seq 1 $2); do
  IFS=, read -ra a <<< "$best"; n=${#a[@]}
  i=$((RANDOM % (n-1))); a[$i]=$((RANDOM % 6))
  cand=$(IFS=,; echo "${a[*]}")
  out=$(uv run python scripts/31_ns_tool.py synth U13 --moves $cand 2>&1 | head -1)
  v=$(echo "$out" | sed -nE 's/.*activation (-?[0-9.]+).*/\1/p')
  [ -z "$v" ] && continue
  if (( $(echo "$v > $bestv" | bc -l) )); then best=$cand; bestv=$v; echo "it $it $best $bestv"; fi
done
echo "final $best $bestv"
