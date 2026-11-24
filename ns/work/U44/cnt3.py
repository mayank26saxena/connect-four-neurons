import sys, re, collections
txt = sys.stdin.read()
blocks = re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]*)  last move.*?\n((?:[.XO]{7}\n){6})", txt, re.S)
C = collections.Counter(); N = 0
for act, mv, bd in blocks:
    g = bd.strip().split("\n")[::-1]
    N += 1
    h = [sum(1 for r in range(6) if g[r][c] != '.') for c in range(7)]
    f = {}
    for r in range(6):
        for p in 'XO':
            if g[r][2] == p and g[r][3] == p and g[r][1] == '.' and g[r][4] == '.':
                f['pair23_' + p] = 1
                if h[1] == r or h[4] == r: f['pair23play1_' + p] = 1
                if h[1] == r and h[4] == r: f['pair23play2_' + p] = 1
            if g[r][3] == p and g[r][4] == p and g[r][2] == '.' and g[r][5] == '.':
                f['pair34_' + p] = 1
    f['h1==h4'] = int(h[1] == h[4])
    f['any23'] = int(any(k.startswith('pair23_') for k in f))
    for k in f: C[k] += f[k]
print(N, ' '.join('%s:%d' % (k, C[k]) for k in sorted(C)))
