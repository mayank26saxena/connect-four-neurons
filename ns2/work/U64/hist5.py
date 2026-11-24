import sys,re
from collections import Counter
for f in sys.argv[1:]:
    ms=[l for l in open(f) if l.startswith('[pos')]
    H=[Counter() for _ in range(7)]; P=Counter(); n=len(ms)
    for l in ms:
        mv=[int(x) for x in re.search(r'moves: ([\d,]+)',l).group(1).split(',')]
        for c in range(7): H[c][mv.count(c)]+=1
        P[len(mv)//4]+=1
    print(f.split('/')[-1],'ply/4',[P[k] for k in range(11)])
    for c in range(7): print('   col',c,[H[c][k] for k in range(7)])
