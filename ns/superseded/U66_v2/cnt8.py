import sys,re,collections
for f in sys.argv[1:]:
    L=open(f).read().split('\n')
    c=collections.Counter(); n=0
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            g=list(reversed(L[i+1:i+7])); n+=1
            for r in range(4):
                for k in range(7):
                    if g[r][k]=='X': c['X%d%d'%(r,k)]+=1
                    if g[r][k]=='O': c['O%d%d'%(r,k)]+=1
    print(f.split('_')[-1],n)
    for p in 'XO':
        for r in range(3,-1,-1):
            print(' ',p,r,' '.join('%3d'%(100*c['%s%d%d'%(p,r,k)]//n) for k in range(7)))
