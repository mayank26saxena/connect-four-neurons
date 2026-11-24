import sys,collections
def load(fs):
    c=collections.Counter(); n=0
    for f in fs:
        L=open(f).read().split('\n')
        for i,l in enumerate(L):
            if l.startswith('[pos'):
                g=list(reversed(L[i+1:i+7])); n+=1
                for r in range(6):
                    for k in range(7):
                        c[(g[r][k],r,k)]+=1
    return c,n
lo,nl=load(['ns/work/U66/ex_b%d.txt'%b for b in (0,1,2,3)])
hi,nh=load(['ns/work/U66/ex_b%d.txt'%b for b in (8,9)])
for p in 'XO.':
    print(p,'  (hi% / lo%)')
    for r in range(5,-1,-1):
        print(r,' '.join('%3d/%3d'%(100*hi[(p,r,k)]//nh,100*lo[(p,r,k)]//nl) for k in range(7)))
