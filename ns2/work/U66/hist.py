import sys
rows = [l.split() for l in open(sys.argv[1])]
by = {}
for bd, mv in rows:
    ms = [int(x) for x in mv.split(',')]
    h = [0]*7
    for m in ms: h[m] += 1
    by.setdefault(bd, []).append((h, len(ms), ms[-1]))
for bd in sorted(by):
    L = by[bd]; n = len(L)
    meanh = [round(sum(x[0][c] for x in L)/n, 1) for c in range(7)]
    full = [round(sum(x[0][c] == 6 for x in L)/n, 2) for c in range(7)]
    ply = round(sum(x[1] for x in L)/n, 1)
    last = [sum(x[2] == c for x in L) for c in range(7)]
    print(bd, n, 'ply', ply, 'meanh', meanh, 'full', full, 'last', last)
