#!/bin/zsh
# usage: last.sh spec lastcol [order]  -> builds board with given top stone (must be O = their) as last move
cd {REPO}
export C4N_CONFIG=ns2 NS_DIR=$PWD/ns2
spec=$1; lc=$2; ord=${3:-3241506}
python3 - "$spec" "$lc" <<'PY' > /tmp/u29spec.txt
import sys
cols=sys.argv[1].split(','); lc=int(sys.argv[2])
assert cols[lc][-1]=='O'
cols[lc]=cols[lc][:-1]
# flip perspective: after removing their stone, the player to move is them -> swap X/O
print(','.join(c.translate(str.maketrans('XO','OX')) for c in cols))
PY
m=$(python3 -I ns2/work/U29/mk.py "$(cat /tmp/u29spec.txt)" $ord)
if [[ $m == IMPOSSIBLE ]]; then echo "$spec last $lc IMPOSSIBLE"; exit; fi
a=$(uv run python scripts/31_ns_tool.py act U29 --moves $m,$lc | grep after | tail -1 | sed 's/.*): //')
echo "$spec last=$lc ord=$ord -> $a [$m,$lc]"
