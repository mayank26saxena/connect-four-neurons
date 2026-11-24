import sys,re
from collections import Counter
feat=sys.argv[1]
for bd in range(10):
    vals=[]
    for l in open(f'ns2/work/U88/ex_b{bd}.txt'):
        if not l.startswith('[pos'): continue
        m=[int(x) for x in re.search(r'moves: ([0-9,]+)',l).group(1).split(',')]
        # heights before each move
        hs=[0]*7; rows=[]
        for c in m: rows.append(hs[c]); hs[c]+=1
        vals.append(eval(feat))
    c=Counter(vals); print(bd,' '.join(f'{k}:{c[k]}' for k in sorted(c)))
