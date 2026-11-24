#!/usr/bin/env bash
# Mid-size models (PLAN addendum m), smallest first; the 6x256 replicates last. Resumable per stage. Logs in runs/ladder/.
set -uo pipefail
cd "$(dirname "$0")/.."
export PATH=$HOME/.local/bin:$PATH
uv run python -c "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 3)" || { echo "no CUDA: refusing to run on CPU" >&2; exit 3; }
mkdir -p runs/ladder
for name in L6d128_s{1..5} L4d192_s{1..5} L4d256_s{1..5} L6d256_s2 L6d256_s3; do
  rd=results/ladder/$name
  for st in 02_train 22_board_causal; do
    [ -f "$rd/.done_$st" ] && continue
    echo "$(date -u +%FT%TZ) start $name $st" >> runs/ladder/mid.log
    if C4N_CONFIG=ladder/$name uv run python -W ignore scripts/$st.py > runs/ladder/${name}_$st.log 2>&1; then
      mkdir -p "$rd"; touch "$rd/.done_$st"; echo "$(date -u +%FT%TZ) done $name $st" >> runs/ladder/mid.log
    else
      echo "$(date -u +%FT%TZ) FAILED $name $st" >> runs/ladder/mid.log
    fi
  done
done
echo "$(date -u +%FT%TZ) mid all done" >> runs/ladder/mid.log
