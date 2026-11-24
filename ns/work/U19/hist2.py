import sys
from collections import Counter
C=Counter()
for r in (l.split() for l in open(sys.argv[1])):
    f = r[5]=="FIRES"
    s=r[r.index("moves:")+1]
    if s=="last": continue
    m=[int(x) for x in s.split(",")]
    h=[0]*7
    for c in m: h[c]+=1
    if len(m) < 18: continue
    C[(f, min(h))]+=1
print(sorted(C.items()))
