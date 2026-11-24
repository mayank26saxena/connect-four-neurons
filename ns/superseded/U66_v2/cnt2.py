import sys,re,collections
for f in sys.argv[1:]:
    L=open(f).read().split('\n')
    c=collections.Counter(); n=0
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            g=list(reversed(L[i+1:i+7])); n+=1
            lc=re.search(r'last move col (\S+)',l).group(1)
            if lc=='None': continue
            lc=int(lc); col=[g[r][lc] for r in range(6) if g[r][lc]!='.']
            h=len(col)
            if lc in (0,6):
                c['edge']+=1
                if h==1: c['edge_bottom']+=1
                elif col[-2]=='O': c['edge_onO']+=1
                else: c['edge_onX']+=1
    print(f,n,dict(c))
