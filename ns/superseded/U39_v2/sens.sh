base=$1
IFS=, read -rA M <<< "$base"
n=${#M[@]}
for ((i=1;i<=n;i++)); do
  line="idx$((i-1)) (was ${M[$i]}):"
  for c in 0 1 2 3 4 5 6; do
    N=("${M[@]}"); N[$i]=$c; s=$(IFS=,; echo "${N[*]}")
    v=$(uv run python scripts/31_ns_tool.py act U39 --moves $s 2>&1 | grep "after *$n moves" | awk '{print $(NF-1)=="FIRES"?$(NF-1):$NF}' )
    v=$(uv run python scripts/31_ns_tool.py act U39 --moves $s 2>&1 | grep "after *$n moves" | grep -oE ': -?[0-9.]+' | tr -d ': ')
    line="$line $c:${v:-ill}"
  done
  echo $line
done
