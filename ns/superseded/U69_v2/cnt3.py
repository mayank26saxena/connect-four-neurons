import re,sys
from collections import defaultdict
txt=open(sys.argv[1]).read().split('\n')
rows=[]
for i,l in enumerate(txt):
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+)',l)
    if m:
        a=float(m.group(2)); grid=txt[i+1:i+7]
        h=[sum(1 for r in grid if r[c]!='.') for c in range(7)]
        rows.append((a,h))
d=defaultdict(list)
for a,h in rows:
    if h[1]==6:
        nf=sum(x==6 for x in h); empt=42-sum(h)
        d[(nf)].append(a)
for k in sorted(d): v=d[k]; print("nfull",k,len(v),"fire",sum(x>3.693 for x in v),"mean %.1f"%(sum(v)/len(v)))
d=defaultdict(list)
for a,h in rows:
    if h[1]==6: d[42-sum(h)].append(a)
for k in sorted(d): v=d[k]; print("empty",k,len(v),"fire",sum(x>3.693 for x in v),"mean %.1f"%(sum(v)/len(v)))
