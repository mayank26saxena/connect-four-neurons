import sys,re,collections
for f in sys.argv[1:]:
    L=open(f).read().split('\n')
    c=collections.Counter(); n=0
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            g=list(reversed(L[i+1:i+7])); n+=1
            h=[sum(g[r][k]!='.' for r in range(6)) for k in range(7)]
            t=[g[h[k]-1][k] if h[k] else '.' for k in range(7)]
            c['h4=2']+=h[4]==2
            c['h4in23']+=h[4] in (2,3)
            c['t4X']+=t[4]=='X'
            c['h4=2&t4X']+=h[4]==2 and t[4]=='X'
            c['h6>=2&t6O']+=h[6]>=2 and t[6]=='O'
            c['h1=0']+=h[1]==0
            c['h5=0']+=h[5]==0
            c['h1=0&h5=0']+=h[1]==0 and h[5]==0
            c['h0=1']+=h[0]==1
    print(f.split('_')[-1],' '.join('%s:%.2f'%(k,c[k]/n) for k in c))
