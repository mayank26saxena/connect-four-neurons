#!/usr/bin/env bash
# Main run on the GPU host: waits for data generation, then every stage in order, one log per stage in runs/.
set -euo pipefail
cd "$(dirname "$0")/.."
export C4N_CONFIG=${C4N_CONFIG:-base}
while pgrep -f "[s]cripts/01_generate_data.py" >/dev/null; do sleep 20; done
[ -f data/analysis.npz ] || uv run python scripts/01_generate_data.py > runs/01_generate_data.log 2>&1
nvidia-smi > runs/nvidia-smi.txt
STAGES=${STAGES:-"02_train 03_eval_play 04_sparsity 05_concepts 06_modes 07_action 07b_group_action 08_dynamics 09_export_web"}
for s in $STAGES; do
  echo "$(date -u +%FT%TZ) start $s" >> runs/main.log
  uv run python -W ignore scripts/$s.py > runs/$s.log 2>&1
  echo "$(date -u +%FT%TZ) done $s" >> runs/main.log
done
node tests/check_web_port.js > runs/check_web_port.log 2>&1
uv run python scripts/manifest.py >> runs/main.log 2>&1
echo "$(date -u +%FT%TZ) all done" >> runs/main.log
