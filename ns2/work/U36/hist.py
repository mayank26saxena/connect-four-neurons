import sys,re,glob
from collections import Counter
def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            rows=L[i+1:i+7]; out.append(rows[::-1])
    return out
feat=sys.argv[1]; cond=sys.argv[2] if len(sys.argv)>2 else "True"
for b in range(10):
    P=parse(f'ns2/work/U36/ex_b{b}.txt'); C=Counter()
    for g in P:
        h=[sum(1 for r in range(6) if g[r][c]!='.') for c in range(7)]
        C[eval(feat)]+=1 if eval(cond) else 0
    print(b, sorted(C.items(),key=lambda x:-x[1])[:8])
