#!/bin/bash
# usage: rep.sh "m0,m1,..." idx col  -> activation with move idx replaced by col
IFS=',' read -ra M <<< "$1"; M[$2]=$3; S=$(IFS=,; echo "${M[*]}")
cd {REPO} && uv run python scripts/31_ns_tool.py act U10 --moves $S 2>&1 | grep after | tail -1
