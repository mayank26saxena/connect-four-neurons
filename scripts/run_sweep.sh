#!/usr/bin/env bash
# Run every configs/sweep/*.yaml (smallest width first), then re-analyse the main model with the current vocabulary.
# Resumable: a stage is skipped when <results_dir>/.done_<stage> exists. One log per run and stage in runs/sweep/.
set -uo pipefail
cd "$(dirname "$0")/.."
export PATH=$HOME/.local/bin:$PATH
mkdir -p runs/sweep
STAGES="02_train 03_eval_play 04_sparsity 05_concepts 06_modes 07_action 07b_group_action"
run_stage () {  # config, results_dir, stage
  local cfg=$1 rd=$2 s=$3
  [ -f "$rd/.done_$s" ] && return 0
  echo "$(date -u +%FT%TZ) start $cfg $s" >> runs/sweep/sweep.log
  if C4N_CONFIG=$cfg uv run python -W ignore scripts/$s.py > "runs/sweep/${cfg//\//_}_$s.log" 2>&1; then
    mkdir -p "$rd"; touch "$rd/.done_$s"; echo "$(date -u +%FT%TZ) done $cfg $s" >> runs/sweep/sweep.log
  else
    echo "$(date -u +%FT%TZ) FAILED $cfg $s" >> runs/sweep/sweep.log
  fi
}
for w in 256 512 1024 2048 4096; do
  for s in 1 2; do
    for st in $STAGES; do run_stage "sweep/w${w}_s${s}" "results/sweep/w${w}_s${s}" "$st"; done
  done
done
for st in 05_concepts 06_modes 07_action 07b_group_action 09_export_web; do run_stage base results "$st"; done
echo "$(date -u +%FT%TZ) sweep all done" >> runs/sweep/sweep.log
echo "$(date -u +%FT%TZ) summary" >> runs/sweep/sweep.log; uv run python scripts/10_sweep_summary.py > runs/sweep/summary.log 2>&1
