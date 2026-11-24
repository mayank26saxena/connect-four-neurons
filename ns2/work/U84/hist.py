import sys,re
def parse(f):
    L=open(f).read().split('\n');out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            rows=L[i+1:i+7]; out.append(rows[::-1])
    return out
for f in sys.argv[1:]:
    bs=parse(f); n=len(bs)
    print(f, n)
    for ch in 'XO.':
        print(' cell',ch)
        for r in range(5,-1,-1):
            print('  ',' '.join('%3d'%(100*sum(b[r][c]==ch for b in bs)//n) for c in range(7)))
    hs=[[sum(b[r][c]!='.' for r in range(6)) for c in range(7)] for b in bs]
    print(' mean heights',[round(sum(h[c] for h in hs)/n,1) for c in range(7)])
