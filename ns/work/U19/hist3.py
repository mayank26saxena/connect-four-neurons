import sys
from collections import Counter
rows=[]
for r in (l.split() for l in open(sys.argv[1])):
    f = r[5]=="FIRES"
    s=r[r.index("moves:")+1]
    if s=="last": continue
    m=[int(x) for x in s.split(",")]
    h=[0]*7
    for c in m: h[c]+=1
    if len(m) < 18: continue
    rows.append((f,h))
for f in (True,False):
    sub=[h for ff,h in rows if ff==f]
    print(f,len(sub))
    for c in range(7):
        cnt=Counter(h[c] for h in sub)
        print(c, [cnt[k] for k in range(7)])
