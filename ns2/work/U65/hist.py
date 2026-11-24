import sys,re
def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            rows=L[i+1:i+7]; m=re.search(r'last move col (\d)',l)
            out.append((rows,int(m.group(1)) if m else -1, len(re.search(r'moves: ([\d,]*)',l).group(1).split(','))))
    return out
for fn in sys.argv[1:]:
    P=parse(fn); n=len(P)
    print(fn, n, 'mean ply', sum(p[2] for p in P)/n)
    for ch in 'XO':
        print(' frac',ch)
        for r in range(6):
            print('  ',' '.join('%3d'%round(100*sum(p[0][r][c]==ch for p in P)/n) for c in range(7)))
    print(' lastcol', [sum(p[1]==c for p in P) for c in range(7)])
