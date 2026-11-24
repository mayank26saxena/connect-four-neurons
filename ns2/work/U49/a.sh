cd {REPO} && export C4N_CONFIG=ns2 NS_DIR={REPO}/ns2
for m in "$@"; do printf "%-40s " "$m"; uv run python scripts/31_ns_tool.py act U49 --moves $m 2>&1 | grep "after" | tail -1 | sed 's/.*://'; done
