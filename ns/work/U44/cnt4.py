import sys, re, collections
txt = sys.stdin.read()
blocks = re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]*)  last move.*?\n((?:[.XO]{7}\n){6})", txt, re.S)
C = collections.Counter(); N = 0
for act, mv, bd in blocks:
    g = bd.strip().split("\n")[::-1]
    N += 1
    h = [sum(1 for r in range(6) if g[r][c] != '.') for c in range(7)]
    d = min(h[2], h[3]) - max(h[1], h[4])
    C['d=%d' % max(-2, min(d, 4))] += 1
    # number of rows r where cells (r,2),(r,3) both filled and (r,1),(r,4) both empty
    k = sum(1 for r in range(6) if g[r][2] != '.' and g[r][3] != '.' and g[r][1] == '.' and g[r][4] == '.')
    C['k=%d' % min(k, 3)] += 1
print(N, ' '.join('%s:%d' % (k, C[k]) for k in sorted(C)))
