#!/usr/bin/env bash
# Train and test every ladder model, smallest first (PLAN addendum l). Resumable per stage. Logs in runs/ladder/.
set -uo pipefail
cd "$(dirname "$0")/.."
export PATH=$HOME/.local/bin:$PATH
uv run python -c "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 3)" || { echo "no CUDA: refusing to run on CPU" >&2; exit 3; }
mkdir -p runs/ladder
for size in L1d64 L1d128 L2d64 L2d128 L3d64; do
  for s in 1 2 3 4 5; do
    name=${size}_s$s; rd=results/ladder/$name
    for st in 02_train 22_board_causal; do
      [ -f "$rd/.done_$st" ] && continue
      echo "$(date -u +%FT%TZ) start $name $st" >> runs/ladder/ladder.log
      if C4N_CONFIG=ladder/$name uv run python -W ignore scripts/$st.py > runs/ladder/${name}_$st.log 2>&1; then
        mkdir -p "$rd"; touch "$rd/.done_$st"; echo "$(date -u +%FT%TZ) done $name $st" >> runs/ladder/ladder.log
      else
        echo "$(date -u +%FT%TZ) FAILED $name $st" >> runs/ladder/ladder.log
      fi
    done
  done
done
echo "$(date -u +%FT%TZ) ladder all done" >> runs/ladder/ladder.log
