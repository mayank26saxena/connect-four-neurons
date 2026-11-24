#!/bin/zsh
# hill-climb by swapping moves i and i+2 in different columns (same player, same board)
cd {REPO}
cur=(${(s:,:)1}); best=$(ns/work/U08/a.sh ${(j:,:)cur} 1 | tr -d ' ')
for it in $(seq 1 $2); do
  n=$(( ${#cur} - 3 ))
  i=$(( (RANDOM % (n - 2)) + 1 ))
  j=$(( i + 2 ))
  [[ ${cur[$i]} == ${cur[$j]} ]] && continue
  new=("${cur[@]}"); t=${new[$i]}; new[$i]=${new[$j]}; new[$j]=$t
  v=$(ns/work/U08/a.sh ${(j:,:)new} 1 | tr -d ' ')
  if (( v > best )); then best=$v; cur=("${new[@]}"); echo "$best ${(j:,:)cur}"; fi
done
echo "FINAL $best ${(j:,:)cur}"
