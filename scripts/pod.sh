#!/usr/bin/env bash
# Helpers for running stages on a remote GPU host. Usage: scripts/pod.sh push|pull|run "<cmd>"
# Host is read from POD_SSH (e.g. "root@1.2.3.4 -p 12345"); the remote copy lives at /workspace/connect4-neurons.
set -euo pipefail
HOST=${POD_SSH:?set POD_SSH="user@host -p port"}
USERHOST=${HOST%% *}; PORT=${HOST##*-p }
SSH="ssh -o StrictHostKeyChecking=accept-new -p $PORT"
REMOTE=/workspace/connect4-neurons
case "$1" in
  push) rsync -rltz --no-owner --no-group -e "$SSH" --exclude .venv --exclude build --exclude data --exclude checkpoints --exclude runs --exclude notes --exclude .git --exclude .pytest_cache --exclude "*.egg-info" ./ "$USERHOST:$REMOTE/" ;;
  pull) rsync -rltz --no-owner --no-group -e "$SSH" "$USERHOST:$REMOTE/"{results,runs,checkpoints,data} ./ ;;
  run) $SSH "$USERHOST" "cd $REMOTE && export PATH=\$HOME/.local/bin:\$PATH && $2" ;;
esac
