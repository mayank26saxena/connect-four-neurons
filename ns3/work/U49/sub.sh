#!/bin/bash
A={REPO}/ns3/work/U49/a.sh
IFS=, read -ra base <<< "$1"
echo "orig $($A $1)"
for ((k=0;k<${#base[@]}-1;k++)); do echo -n "k=$k(${base[$k]}): "; for c in 0 1 2 3 4 5 6; do s=("${base[@]}"); s[$k]=$c; m=$(IFS=,; echo "${s[*]}"); printf "%s:%6s " $c "$($A $m)"; done; echo; done
