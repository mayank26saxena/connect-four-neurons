cd {REPO}
export C4N_CONFIG=ns3 NS_DIR={REPO}/ns3
for a in 0 1 2 3 4 5 6; do for b in 0 1 2 3 4 5 6; do for c in 0 1 2 3 4 5 6; do
v=$(uv run python scripts/31_ns_tool.py act U45 --moves $a,$b,$c,4 2>&1 | grep 'after  4' | sed 's/.*: //')
echo "$a $b $c $v"
done; done; done > ns3/work/U45/sweep_last4.txt
