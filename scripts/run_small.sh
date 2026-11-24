#!/usr/bin/env bash
# Train and test the 5 small models (PLAN addendum k). Resumable per stage. Logs in runs/small/.
set -uo pipefail
cd "$(dirname "$0")/.."
export PATH=$HOME/.local/bin:$PATH
uv run python -c "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 3)" || { echo "no CUDA: refusing to run on CPU" >&2; exit 3; }
mkdir -p runs/small
for s in 1 2 3 4 5; do
  for st in 02_train 22_board_causal; do
    rd=results/small/s$s
    [ -f "$rd/.done_$st" ] && continue
    echo "$(date -u +%FT%TZ) start s$s $st" >> runs/small/small.log
    if C4N_CONFIG=small/s$s uv run python -W ignore scripts/$st.py > runs/small/s${s}_$st.log 2>&1; then
      mkdir -p "$rd"; touch "$rd/.done_$st"; echo "$(date -u +%FT%TZ) done s$s $st" >> runs/small/small.log
    else
      echo "$(date -u +%FT%TZ) FAILED s$s $st" >> runs/small/small.log
    fi
  done
done
echo "$(date -u +%FT%TZ) small all done" >> runs/small/small.log
