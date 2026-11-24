import sys, re
from collections import defaultdict, Counter
band=None; C=defaultdict(Counter); n=Counter()
for line in sys.stdin:
    m=re.match(r'=== band (\d)',line)
    if m: band=int(m.group(1)); continue
    m=re.search(r'moves: ([\d,]+)',line)
    if m:
        mv=[int(x) for x in m.group(1).split(',')]
        lc=mv[-1]; lr=mv[:-1].count(lc)
        n[band]+=1; C[band][(lr,lc)]+=1
for b in sorted(n):
    print('band',b,n[b])
    for r in range(5,-1,-1):
        print('  '+' '.join('%3d'%C[b][(r,c)] for c in range(7)))
