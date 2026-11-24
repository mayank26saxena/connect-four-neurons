for m in "$@"; do
 echo "$m => $(uv run python scripts/31_ns_tool.py act U39 --moves $m | grep after | sed -E 's/.*\): (-?[0-9.]+)( FIRES)?.*/\1\2/' | sed 's/ FIRES/*/' | tr '\n' ' ')"
done
