import sys,re,collections
def H(m): return [m.count(c) for c in range(7)]
for fn in sys.argv[1:]:
    ms=[]
    for l in open(fn):
        if l.startswith('[pos'):
            mv=re.search(r'moves:(.*?)last move',l).group(1).strip(); ms.append([int(x) for x in mv.split(',')] if mv else [])
    for lo,hi in ((6,10),(11,15),(16,22)):
        d=[H(m) for m in ms if lo<=len(m)<=hi]
        if not d: continue
        R=[sum(abs(h[c]-h[c+1]) for c in range(6)) for h in d]
        E=[sum(x==0 for x in h) for h in d]
        print(fn,lo,hi,len(d),'rough %.2f'%(sum(R)/len(R)),'empties %.2f'%(sum(E)/len(E)), 'maxh %.2f'%(sum(max(h) for h in d)/len(d)))
