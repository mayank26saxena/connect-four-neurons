import sys, re
from collections import defaultdict, Counter
band=None
H=defaultdict(lambda:[Counter() for _ in range(7)]); P=defaultdict(Counter); L=defaultdict(Counter); n=Counter()
for line in sys.stdin:
    m=re.match(r'=== band (\d)',line)
    if m: band=int(m.group(1)); continue
    m=re.search(r'moves: ([\d,]+)\s+last move col (\d)',line)
    if m:
        mv=[int(x) for x in m.group(1).split(',')]
        n[band]+=1
        P[band][min(len(mv)//4,8)]+=1
        L[band][int(m.group(2))]+=1
        h=[mv.count(c) for c in range(7)]
        for c in range(7): H[band][c][min(h[c],6)]+=1
for b in sorted(n):
    print('band',b,'n',n[b],'ply//4',dict(sorted(P[b].items())),'last',dict(sorted(L[b].items())))
    for c in range(7): print('  col',c,[H[b][c][k] for k in range(7)])
