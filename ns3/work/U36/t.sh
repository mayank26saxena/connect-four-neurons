#!/bin/bash
cd {REPO}
export C4N_CONFIG=ns3 NS_DIR={REPO}/ns3
for s in "$@"; do uv run python scripts/31_ns_tool.py act U36 --moves $s | grep "after.*($s)"; done
