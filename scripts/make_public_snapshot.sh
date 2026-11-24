#!/usr/bin/env bash
# Build a public copy of this repository with fresh history: the files tracked at HEAD, one commit, no remote.
# The private repository keeps the full history (earlier commits contain machine-specific paths that were redacted on 2026-11-24).
# Usage: scripts/make_public_snapshot.sh [OUT_DIR]   (default build/public-repo). It never pushes or creates a GitHub repository.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
OUT=${1:-build/public-repo}
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then echo "commit or stash tracked changes first" >&2; exit 1; fi
if git grep -qE "/Users/[A-Za-z0-9_.-]+/" -- ':!scripts/make_public_snapshot.sh'; then
  echo "absolute home-folder paths are still tracked:" >&2; git grep -lE "/Users/[A-Za-z0-9_.-]+/" -- ':!scripts/make_public_snapshot.sh' >&2; exit 1; fi
SRC=$(git rev-parse --short HEAD)
rm -rf "$OUT"; mkdir -p "$OUT"
git archive HEAD | tar -x -C "$OUT"
cd "$OUT"
git init -q -b main
git add -A
git -c user.name="$(git -C "$OLDPWD" config user.name)" -c user.email="$(git -C "$OLDPWD" config user.email)" \
  commit -q -m "Connect Four neurons: code, results and write-up (snapshot of private repository commit $SRC)"
echo "public snapshot ready in $OUT ($(git ls-files | wc -l | tr -d ' ') files, one commit from $SRC); nothing was pushed"
