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
        g='hi' if band>=7 else 'lo'
        k=(g, len(mv)%2)
        n[k]+=1; C[k][(lr,lc)]+=1
for k in sorted(n):
    print(k,'(ply parity; 0 = me first)',n[k])
    for r in range(5,-1,-1):
        print('  '+' '.join('%3d'%C[k][(r,c)] for c in range(7)))
