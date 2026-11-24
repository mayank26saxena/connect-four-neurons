import sys,re
from collections import defaultdict,Counter
# reads examples output on stdin; prints per-band histograms of single features
band=None; recs=defaultdict(list)
for line in sys.stdin:
    m=re.match(r'=== band (\d)',line)
    if m: band=int(m.group(1)); continue
    m=re.search(r'moves: ([\d,]+)\s+last move col (\d)',line)
    if m and band is not None:
        mv=[int(x) for x in m.group(1).split(',')]
        h=[mv.count(c) for c in range(7)]
        recs[band].append((len(mv),h,int(m.group(2)),'must-block []' not in line))
feat=sys.argv[1]
for b in sorted(recs):
    c=Counter()
    for ply,h,lc,mb in recs[b]:
        if feat=='parity': c[ply%2]+=1
        elif feat=='ply': c[ply//8]+=1
        elif feat=='minh': c[min(h)]+=1
        elif feat=='empty': c[h.count(0)]+=1
        elif feat=='mb': c[mb]+=1
        elif feat=='lastc': c[lc]+=1
        elif feat=='lasth': c[h[lc]]+=1
        elif feat=='h3': c[h[3]]+=1
        elif feat=='h5': c[h[5]]+=1
        elif feat=='h4': c[h[4]]+=1
        elif feat=='h2': c[h[2]]+=1
    print(b,len(recs[b]),sorted(c.items()))
