import sys, re
def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            g=L[i+1:i+7]; moves=re.search(r'moves: ([\d,]*)',l).group(1)
            out.append((g[::-1], [int(x) for x in moves.split(',')], re.search(r'last move col (\d)',l)))
    return out
groups={'low':['0','1','2'],'high':['6','7','8','9']}
for name,bs in groups.items():
    P=[p for b in bs for p in parse(f'ex_b{b}.txt')]
    n=len(P); print(name,n)
    for sym in 'XO':
        print(' cell freq',sym)
        for r in range(5,-1,-1):
            print('  ',' '.join('%3d'%round(100*sum(p[0][r][c]==sym for p in P)/n) for c in range(7)))
    import collections
    ply=collections.Counter(min(len(p[1])//5,7) for p in P); print(' ply/5',sorted(ply.items()))
    lc=collections.Counter(p[1][-1] for p in P); print(' lastcol',sorted(lc.items()))
    par=collections.Counter(len(p[1])%2 for p in P); print(' parity',sorted(par.items()))
    lr=collections.Counter()
    for p in P:
        c=p[1][-1]; h=sum(p[0][r][c]!='.' for r in range(6)); lr[h-1]+=1
    print(' lastrow',sorted(lr.items()))
