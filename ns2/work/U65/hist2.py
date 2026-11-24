import sys,re
def parse(fns,maxply):
    out=[]
    for fn in fns:
        L=open(fn).read().split('\n')
        for i,l in enumerate(L):
            if l.startswith('[pos'):
                n=len(re.search(r'moves: ([\d,]*)',l).group(1).split(','))
                if n<=maxply: out.append((L[i+1:i+7],n))
    return out
for name,fns in [('low',['b0.txt','b1.txt','b2.txt']),('high',['b7.txt','b8.txt','b9.txt'])]:
    P=parse(fns,14); n=len(P); print(name,n,'mean ply',sum(p[1] for p in P)/n)
    for ch in 'XO':
        print(' frac',ch)
        for r in range(6):
            print('  ',' '.join('%3d'%round(100*sum(p[0][r][c]==ch for p in P)/n) for c in range(7)))
