import sys,re
from collections import Counter
for f in sys.argv[1:]:
    txt=open(f).read(); C=Counter(); n=0
    for m in re.finditer(r'moves: ([\d,]+)',txt):
        mv=[int(x) for x in m.group(1).split(',')]; n+=1
        lc=mv[-1]; lr=mv.count(lc)-1; C[(lr,lc)]+=1
    print(f,n)
    for r in range(5,-1,-1): print(' '.join('%3d'%C[(r,c)] for c in range(7)))
