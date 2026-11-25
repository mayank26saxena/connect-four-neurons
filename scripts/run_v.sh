#!/usr/bin/env bash
# PLAN.md addendum (v) on the GPU host: V1-V5, V6-V7, then the V8 organisms. One log per stage in runs/.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p runs
uv run python -c "import torch; assert torch.cuda.is_available(), 'no CUDA'; print(torch.cuda.get_device_name(0))" > runs/v_cuda.txt
stage() {
  local name=$1; shift
  echo "$(date -u +%FT%TZ) start $name" >> runs/v.log
  uv run python -W ignore "$@" > "runs/$name.log" 2>&1 || { echo "$(date -u +%FT%TZ) FAILED $name" >> runs/v.log; exit 1; }
  echo "$(date -u +%FT%TZ) done $name" >> runs/v.log
}
stage 48_readouts scripts/48_readouts.py
stage 49_neuron_tools scripts/49_neuron_tools.py
stage 50_train scripts/50_organisms.py train
stage 50_analyze scripts/50_organisms.py analyze
echo "$(date -u +%FT%TZ) all done" >> runs/v.log
