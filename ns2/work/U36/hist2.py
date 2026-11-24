import sys,re
from collections import Counter
def parse(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            mv=[int(x) for x in re.search(r'moves: ([\d,]+)',l).group(1).split(',')]
            out.append((L[i+1:i+7][::-1],mv))
    return out
feat=sys.argv[1]; cond=sys.argv[2] if len(sys.argv)>2 else "True"
for b in range(10):
    C=Counter()
    for g,mv in parse(f'ns2/work/U36/ex_b{b}.txt'):
        h=[sum(1 for r in range(6) if g[r][c]!='.') for c in range(7)]
        if eval(cond): C[eval(feat)]+=1
    print(b, sorted(C.items(),key=lambda x:-x[1])[:8])
