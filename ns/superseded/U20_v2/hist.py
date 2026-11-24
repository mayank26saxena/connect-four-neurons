import sys,re
def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            g=L[i+1:i+7]; mv=re.search(r'moves: ([\d,]*)',l).group(1); out.append((g,mv,l))
    return out
for fn in sys.argv[1:]:
    P=parse(fn); n=len(P); print(fn,n)
    for ch in 'XO.':
        print(ch)
        for r in range(6):
            print(' '.join('%3d'%(100*sum(p[0][r][c]==ch for p in P)//n) for c in range(7)))
    import collections
    print('ply', sorted(collections.Counter(len(p[1].split(',')) for p in P).items()))
    print('lastcol', sorted(collections.Counter(re.search(r'last move col (\S+)',p[2]).group(1) for p in P).items()))
