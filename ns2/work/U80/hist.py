import sys,re
from collections import Counter
for f in sys.argv[1:]:
    txt=open(f).read()
    hs=[Counter() for _ in range(7)]; last=Counter(); par=Counter(); n=0
    for m in re.finditer(r'moves: ([\d,]+)\s+last move col (\d)',txt):
        mv=[int(x) for x in m.group(1).split(',')]; n+=1
        h=[mv.count(c) for c in range(7)]
        for c in range(7): hs[c][min(h[c],6)]+=1
        last[int(m.group(2))]+=1; par[len(mv)%2]+=1
    print(f,n,'last',sorted(last.items()),'parity',sorted(par.items()))
    for c in range(7): print('  col',c,[hs[c][k] for k in range(7)])
