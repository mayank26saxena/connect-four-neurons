#!/bin/zsh
# for sequence $1, replace move at index i with each column, print
cd {REPO}
s=$1; i=$2
arr=(${(s:,:)s})
L=""
for c in 0 1 2 3 4 5 6; do arr2=($arr); arr2[$i]=$c; L="$L ${(j:,:)arr2}"; done
ns2/work/U59/a.sh $=L
