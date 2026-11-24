import sys,re,collections
for f in sys.argv[1:]:
    L=open(f).read().split('\n')
    H=[collections.Counter() for _ in range(7)]; n=0; full=collections.Counter()
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            g=list(reversed(L[i+1:i+7])); n+=1
            for c in range(7):
                h=sum(g[r][c]!='.' for r in range(6)); H[c][h]+=1
                if h==6: full[c]+=1
    print(f.split('_')[-1], ' '.join('c%d:%s'%(c,''.join('%2d'%(H[c][h]*100//n//10) for h in range(7))) for c in range(7)))
