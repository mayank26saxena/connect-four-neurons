import sys,re,collections
exec(open('h4.py').read().split('P=parse')[0])
H=lambda g,c: sum(g[r][c]!='.' for r in range(6))
def feats(g,lc,mv):
    ply=0 if mv=='' else len(mv.split(','))
    return dict(h2=min(H(g,2),3), col1=g[0][1]+g[1][1], c00=g[0][0], lc=lc, par=ply%2, h3=min(H(g,3),3), plyb=min(ply//6,4),
       h4=min(H(g,4),3), h5=min(H(g,5),2), h6=min(H(g,6),2), r10=g[1][0], r12=g[1][2], r02=g[0][2])
for fn in sys.argv[1:]:
  P=[p for p in parse(fn) if H(p[0],1)==2 and H(p[0],0)<2]
  print(fn,len(P))
  F=[feats(g,lc,mv) for g,a,lc,mv in P]
  for k in F[0]:
    c=collections.Counter(f[k] for f in F); n=len(F)
    print(' ',k, ' '.join('%s:%d'%(v,100*c[v]//n) for v in sorted(c)))
