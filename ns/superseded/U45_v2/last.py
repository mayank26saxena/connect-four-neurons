import sys,re,collections
for fn in sys.argv[1:]:
    ms=[]
    for l in open(fn):
        if l.startswith('[pos'):
            mv=re.search(r'moves:(.*?)last move',l).group(1).strip(); ms.append([int(x) for x in mv.split(',')] if mv else [])
    ms=[m for m in ms if 6<=len(m)<=20 and 2 not in m]
    T=collections.Counter()
    for m in ms:
        c=m[-1]; r=m.count(c)-1; T[(r,c)]+=1
    n=len(ms); print(fn,n)
    for r in range(5,-1,-1): print('  ',' '.join('%4.2f'%(T[(r,c)]/n) for c in range(7)))
