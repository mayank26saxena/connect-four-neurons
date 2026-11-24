import sys, re, collections
txt = sys.stdin.read()
blocks = re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]*)  last move.*?\n((?:[.XO]{7}\n){6})", txt, re.S)
C = collections.Counter()
for act, mv, bd in blocks:
    g = bd.strip().split("\n")[::-1]
    a = b2 = 0
    for r in range(5):
        for c in range(6):
            if g[r][c] == 'X' and g[r][c+1] == 'X' and g[r+1][c] == 'O' and g[r+1][c+1] == 'O': a += 1
            if g[r][c] == 'O' and g[r][c+1] == 'O' and g[r+1][c] == 'X' and g[r+1][c+1] == 'X': b2 += 1
    C['OOoverXX=%d' % min(a,2)] += 1
    C['XXoverOO=%d' % min(b2,2)] += 1
    C['either=%d' % (a+b2>0)] += 1
print(' '.join('%s:%d' % (k, C[k]) for k in sorted(C)))
