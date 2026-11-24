# per-cell occupancy histogram from examples text on stdin (me=X / them=O), grouped by band
import sys, re
from collections import defaultdict
cnt=defaultdict(lambda: [[[0,0,0] for c in range(7)] for r in range(6)])
n=defaultdict(int)
band=None; rows=[]
for line in sys.stdin:
    m=re.match(r'=== band (\d)',line)
    if m: band=int(m.group(1)); continue
    if re.match(r'^[.XO]{7}$',line.strip()):
        rows.append(line.strip())
        if len(rows)==6:
            n[band]+=1
            for i,rw in enumerate(rows):
                r=5-i
                for c,ch in enumerate(rw):
                    cnt[band][r][c]['.XO'.index(ch)]+=1
            rows=[]
for bd in sorted(n):
    print('band',bd,'n',n[bd])
    for r in range(5,-1,-1):
        print(' '.join('%3d/%3d'%(100*cnt[bd][r][c][1]//n[bd],100*cnt[bd][r][c][2]//n[bd]) for c in range(7)))
