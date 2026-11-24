import sys, re, collections
def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            mv=re.search(r'moves:(.*?)last move',l).group(1).strip()
            mv=[int(x) for x in mv.split(',')] if mv else []
            rows=L[i+1:i+7]
            out.append((mv,rows))
    return out
for fn in sys.argv[1:]:
    d=parse(fn); n=len(d)
    H=[[0]*8 for _ in range(7)]; plies=collections.Counter(); last=collections.Counter(); par=collections.Counter()
    for mv,rows in d:
        h=[0]*7
        for c in mv: h[c]+=1
        for c in range(7): H[c][min(h[c],7)]+=1
        plies[len(mv)//4*4]+=1; last[mv[-1] if mv else None]+=1; par[len(mv)%2]+=1
    print(fn,n)
    for c in range(7): print(' col',c,'height hist',H[c][:7])
    print(' ply',sorted(plies.items())); print(' last',sorted(last.items(),key=str)); print(' parity',par)
