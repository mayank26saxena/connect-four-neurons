import sys, re, collections
txt = sys.stdin.read()
blocks = re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]*)  last move.*?\n((?:[.XO]{7}\n){6})", txt, re.S)
C = collections.Counter(); N = 0
for act, mv, bd in blocks:
    g = bd.strip().split("\n")[::-1]
    N += 1
    h = [sum(1 for r in range(6) if g[r][c] != '.') for c in range(7)]
    for a in range(0, 6):
        lo = [x for x in (a - 1, a + 2) if 0 <= x <= 6]
        d = min(h[a], h[a + 1]) - max(h[x] for x in lo)
        if d >= 2: C['t%d%d' % (a, a + 1)] += 1
print(N, ' '.join('%s:%d' % (k, C[k]) for k in sorted(C)))
