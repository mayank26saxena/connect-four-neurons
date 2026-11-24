#!/usr/bin/env bash
# Concept-mapping comparison (PLAN addendum o): main model first, then the small models. Resumable per stage. Logs in runs/concept/.
set -uo pipefail
cd "$(dirname "$0")/.."
export PATH=$HOME/.local/bin:$PATH
uv run python -c "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 3)" || { echo "no CUDA: refusing to run on CPU" >&2; exit 3; }
mkdir -p runs/concept
run_stage () {  # config, results_dir, stage
  local cfg=$1 rd=$2 st=$3
  [ -f "$rd/.done_$st" ] && return 0
  echo "$(date -u +%FT%TZ) start $cfg $st" >> runs/concept/concept.log
  if C4N_CONFIG=$cfg uv run python -W ignore scripts/$st.py > "runs/concept/${cfg//\//_}_$st.log" 2>&1; then
    mkdir -p "$rd"; touch "$rd/.done_$st"; echo "$(date -u +%FT%TZ) done $cfg $st" >> runs/concept/concept.log
  else
    echo "$(date -u +%FT%TZ) FAILED $cfg $st" >> runs/concept/concept.log
  fi
}
SMOKE=${SMOKE:-} run_stage base results 24_concept_coverage
for name in L4d192_s1 L6d128_s1 L4d192_s2 L6d128_s2 L4d192_s3; do
  for st in 02_train 22_board_causal 14_crossfit 24_concept_coverage; do run_stage concept/$name results/concept/$name $st; done
done
echo "$(date -u +%FT%TZ) concept all done" >> runs/concept/concept.log
