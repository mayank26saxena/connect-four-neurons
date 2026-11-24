import sys,re
def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            g=L[i+1:i+7]; out.append((l,g))
    return out
for fn in sys.argv[1:]:
    P=parse(fn); n=len(P)
    print(fn,n)
    for sym in 'XO':
        print(' cell freq',sym)
        for r in range(6):
            row=[sum(1 for _,g in P if g[r][c]==sym)/n for c in range(7)]
            print('  ','  '.join('%.2f'%x for x in row))
    plies=[sum(ch!='.' for row in g for ch in row) for _,g in P]
    print(' mean ply %.1f'%(sum(plies)/n))
