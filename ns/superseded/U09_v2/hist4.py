import sys,re,collections
txt=open('ns/work/U09/ex_cache.txt').read()
blocks=re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]+).*?\n((?:[.XO]{7}\n){6})",txt)
D=[(0,1),(1,0),(1,1),(1,-1)]
def threats(g,p):
    out=set()
    for r in range(6):
        for c in range(7):
            if g[r][c]!='.':continue
            for dr,dc in D:
                n=1
                for s in (1,-1):
                    k=1
                    while 0<=r+s*k*dr<6 and 0<=c+s*k*dc<7 and g[r+s*k*dr][c+s*k*dc]==p: n+=1;k+=1
                if n>=4: out.add((r,c))
    return out
seen=set();H=collections.defaultdict(collections.Counter);N=collections.Counter()
for a,m,g in blocks:
    if m in seen: continue
    seen.add(m);a=float(a);rows=g.split()[::-1]
    band = 'hi' if a>2 else ('fire' if a>0.909 else 'non')
    t=threats(rows,'O');h=[sum(rows[r][c]!='.' for r in range(6)) for c in range(7)]
    bad=0
    for c in range(7):
        if h[c]<6 and h[c]+1<6 and (h[c]+1,c) in t: bad+=1
    mb=sum(1 for c in range(7) if h[c]<6 and (h[c],c) in t)
    N[band]+=1;H[band][('nt',min(len(t),3))]+=1;H[band][('bad',min(bad,2))]+=1;H[band][('mb',min(mb,2))]+=1
for b in ('non','fire','hi'):
    print(b,N[b],sorted((k,round(100*v/N[b])) for k,v in H[b].items()))
