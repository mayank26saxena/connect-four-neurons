# usage: hist.sh band ; prints per-column height histograms and owner of bottom of col 4 (me/them)
b=$1
uv run python scripts/31_ns_tool.py examples U18 --band $b --n 40 --seed 7 2>&1 | grep "^\[pos" | sed 's/.*moves: \([0-9,]*\).*/\1/' > /tmp/u18_mv_$b.txt
for c in 0 1 2 3 4 5 6; do printf "col$c: "; while read mv; do echo "$mv" | tr ',' '\n' | grep -c "^$c$"; done < /tmp/u18_mv_$b.txt | sort -n | uniq -c | tr '\n' ' '; echo; done
printf "owner (0,4) first-mover-index parity vs ply: "
while read mv; do n=$(echo "$mv" | tr ',' '\n' | wc -l); i=$(echo "$mv" | tr ',' '\n' | grep -n '^4$' | head -1 | cut -d: -f1); if [ -z "$i" ]; then echo none; else if [ $(( (n - i) % 2 )) -eq 0 ]; then echo them; else echo me; fi; fi; done < /tmp/u18_mv_$b.txt | sort | uniq -c | tr '\n' ' '; echo
