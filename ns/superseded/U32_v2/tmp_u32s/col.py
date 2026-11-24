import sys,re
from collections import Counter
def parse(fn):
    L=open(fn).read().split('\n'); out=[]; i=0
    while i<len(L):
        m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+)',L[i])
        if m:
            rows=L[i+1:i+7]; out.append((int(m.group(1)),float(m.group(2)),rows[::-1])); i+=7
        else: i+=1
    return out
d={}
for fn in sys.argv[2:]:
    for p,a,r in parse(fn): d[p]=(a,r)
col=int(sys.argv[1])
for name,sel in [('top>2',lambda a:a>2),('fire',lambda a:0.906<a<=2),('low<0.4',lambda a:a<0.4)]:
    c=Counter(''.join(r[k][col] for k in range(6)).rstrip('.') or '-' for a,r in d.values() if sel(a))
    print(name, sum(c.values()), c.most_common(12))
