import sys,re,collections
for f in sys.argv[1:]:
    L=open(f).read().split('\n')
    c=collections.Counter(); n=0
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            g=list(reversed(L[i+1:i+7])); n+=1
            for col in range(7):
                st=[g[r][col] for r in range(6) if g[r][col]!='.']
                if st and st[-1]=='X': c['topX%d'%col]+=1
                if st and st[-1]=='O': c['topO%d'%col]+=1
    print(f,n,' '.join('%s:%.2f'%(k,c[k]/n) for k in sorted(c)))
