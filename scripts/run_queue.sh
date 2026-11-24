#!/usr/bin/env bash
# usage: run_queue.sh "<stages>" <config> [<config> ...]
# Resumable (a stage is skipped when <results_dir>/.done_<stage> exists); one log per config and stage in runs/queue/.
set -uo pipefail
cd "$(dirname "$0")/.."
export PATH=$HOME/.local/bin:$PATH
mkdir -p runs/queue
STAGES=$1; shift
for cfg in "$@"; do
  rd=$(C4N_CONFIG=$cfg uv run python -c "from c4n import config; print(config.load().get('results_dir','results'))")
  for st in $STAGES; do
    [ -f "$rd/.done_$st" ] && continue
    echo "$(date -u +%FT%TZ) start $cfg $st" >> runs/queue/queue.log
    if C4N_CONFIG=$cfg uv run python -W ignore scripts/$st.py > "runs/queue/${cfg//\//_}_$st.log" 2>&1; then
      mkdir -p "$rd"; touch "$rd/.done_$st"; echo "$(date -u +%FT%TZ) done $cfg $st" >> runs/queue/queue.log
    else
      echo "$(date -u +%FT%TZ) FAILED $cfg $st" >> runs/queue/queue.log
    fi
  done
done
echo "$(date -u +%FT%TZ) queue finished" >> runs/queue/queue.log
