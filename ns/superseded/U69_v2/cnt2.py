import re,sys
from collections import defaultdict
txt=open(sys.argv[1]).read().split('\n')
rows=[]
for i,l in enumerate(txt):
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+)',l)
    if m:
        a=float(m.group(2)); grid=txt[i+1:i+7]
        h=[sum(1 for r in grid if r[c]!='.') for c in range(7)]
        rows.append((a,h,grid))
d=defaultdict(lambda:[0,0])
for a,h,g in rows:
    if h[1]==6:
        k=sum(h)
        d[k][0]+=1; d[k][1]+=a>3.693
for k in sorted(d): print("ply",k,d[k])
# what ply did column 1 become full? unknown; top-of-col1 owner
e=defaultdict(lambda:[0,0])
for a,h,g in rows:
    if h[1]==6:
        k=(g[0][1], sum(h)%2)
        e[k][0]+=1; e[k][1]+=a>3.693
print(dict(e))
