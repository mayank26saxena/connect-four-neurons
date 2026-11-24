# exploration counts: threat features among column-1-full example positions
import re,sys
sys.path.insert(0,'.')
from collections import defaultdict
from c4n.ns import board_from_moves
txt=open(sys.argv[1]).read().split('\n')
d=defaultdict(lambda:[0,0])
for l in txt:
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+).*moves: ([\d,]+)',l)
    if not m: continue
    a=float(m.group(2)); b=board_from_moves([int(x) for x in m.group(3).split(',')])
    if b.heights[1]!=6: continue
    mw=len(b.my_wins); tw=len(b.their_wins)
    k=(b.me_first, min(mw,2), min(tw,2))
    d[k][0]+=1; d[k][1]+=a>3.693
for k in sorted(d): print("me_first,mythreats,theirthreats",k,d[k])
