# usage: scan.sh 2,3,3,...  -> for each move index, replace with each other column, print final activation
cd {REPO} && export C4N_CONFIG=ns2 NS_DIR={REPO}/ns2
IFS=',' read -rA M <<< "$1"
n=${#M[@]}
for ((i=1;i<=n;i++)); do
  line="idx $((i-1)) (orig ${M[$i]}):"
  for c in 0 1 2 3 4 5 6; do
    [[ $c == ${M[$i]} ]] && continue
    N=("${M[@]}"); N[$i]=$c; s=$(IFS=,; echo "${N[*]}")
    out=$(uv run python scripts/31_ns_tool.py act U28 --moves $s 2>&1 | grep "after *$n moves" | sed 's/.*): //;s/ FIRES//')
    line="$line $c=${out:-X}"
  done
  echo $line
done
