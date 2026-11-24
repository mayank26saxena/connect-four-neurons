import sys,re,collections
for f in sys.argv[1:]:
    L=open(f).read().split('\n')
    c=collections.Counter(); n=0
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            g=list(reversed(L[i+1:i+7]))
            lc=re.search(r'last move col (\S+)',l).group(1)
            if lc=='None': continue
            lc=int(lc); h=sum(g[r][lc]!='.' for r in range(6)); n+=1
            c[(h-1,lc)]+=1
    print(f.split('_')[-1],n,sorted(c.items(),key=lambda x:-x[1])[:12])
