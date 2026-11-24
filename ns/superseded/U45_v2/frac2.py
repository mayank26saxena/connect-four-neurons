import sys,re
def H(m): return [m.count(c) for c in range(7)]
feats={
 'cliff3':lambda h:any(abs(h[c]-h[c+1])>=3 for c in range(6)),
 'cliff3_nextto_empty':lambda h:any((h[c]==0 and h[c+1]>=3) or (h[c+1]==0 and h[c]>=3) for c in range(6)),
 'h2in05':lambda h:h[2] in (0,5),
 'h2==0':lambda h:h[2]==0,
 'h2==0&cliff3':lambda h:h[2]==0 and any(abs(h[c]-h[c+1])>=3 for c in range(6)),
 'h2==0&h3>=2':lambda h:h[2]==0 and h[3]>=2,
}
for fn in sys.argv[1:]:
    ms=[]
    for l in open(fn):
        if l.startswith('[pos'):
            mv=re.search(r'moves:(.*?)last move',l).group(1).strip(); ms.append([int(x) for x in mv.split(',')] if mv else [])
    ms=[m for m in ms if 6<=len(m)<=20]
    print(fn,len(ms),{k:round(sum(f(H(m)) for m in ms)/len(ms),2) for k,f in feats.items()})
