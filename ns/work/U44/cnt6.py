import sys, re, collections
txt = sys.stdin.read()
blocks = re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]*)  last move.*?\n((?:[.XO]{7}\n){6})", txt, re.S)
C = collections.Counter(); N = 0
for act, mv, bd in blocks:
    g = bd.strip().split("\n")[::-1]
    N += 1
    n = 0
    for r in range(5):
        for c in range(6):
            if g[r][c] == 'X' and g[r][c+1] == 'X' and g[r+1][c] == 'O' and g[r+1][c+1] == 'O':
                # top-row flanks empty
                l = g[r+1][c-1] if c > 0 else '#'
                rr = g[r+1][c+2] if c < 5 else '#'
                if l == '.' and rr == '.': n += 1
    C['n=%d' % min(n, 2)] += 1
print(N, ' '.join('%s:%d' % (k, C[k]) for k in sorted(C)))
