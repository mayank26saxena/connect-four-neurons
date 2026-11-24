import sys,re
def parse(fn):
    L=open(fn).read().split('\n'); out={}
    for l in L:
        if l.startswith('[pos'):
            pid=int(re.search(r'pos (\d+)',l).group(1))
            mv=re.search(r'moves:(.*?)last move',l).group(1).strip()
            out[pid]=[int(x) for x in mv.split(',')] if mv else []
    return list(out.values())
def grid(mv):
    g=[[0]*7 for _ in range(6)]; h=[0]*7; me=len(mv)%2
    for i,c in enumerate(mv):
        g[h[c]][c]=1 if i%2==me else 2; h[c]+=1
    return g
filt=lambda m: 6<=len(m)<=20 and 2 not in m
for fn in sys.argv[1:]:
    d=[m for m in parse(fn) if filt(m)]; n=len(d)
    print(fn,n)
    for who,lab in ((1,'mine'),(2,'theirs')):
        print(' ',lab)
        for r in range(4,-1,-1):
            print('   ',' '.join('%4.2f'%(sum(grid(m)[r][c]==who for m in d)/n) for c in range(7)))
    import collections
    print('  last col',sorted(collections.Counter(m[-1] for m in d).items()))
    print('  parity me_first',sum(len(m)%2==0 for m in d)/n)
