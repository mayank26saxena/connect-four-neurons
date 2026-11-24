import sys, re
txt = open(sys.argv[1]).read().split("\n")
i = 0
seen = set()
while i < len(txt):
    m = re.match(r"\[pos (\d+)\] pole act ([-0-9.]+).*moves: ([0-9,]*)\s+last move col (\S+)", txt[i])
    if m:
        pos, act, mv, lc = m.groups()
        rows = txt[i+1:i+7]
        if pos not in seen:
            seen.add(pos)
            g = [rows[5-r] for r in range(6)]
            cols = {c: "".join(g[r][c] for r in range(6)).rstrip(".") for c in range(7)}
            ply = len([x for x in mv.split(",") if x])
            print(f"{float(act):6.2f} ply{ply:2d} last{lc:>4} c3={cols[3]:<6} c4={cols[4]:<6} c5={cols[5]:<6} c6={cols[6]:<6}")
        i += 7
    else:
        i += 1
