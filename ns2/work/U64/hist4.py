import sys,re
from collections import Counter
for f in sys.argv[1:]:
    ms=[l for l in open(f) if l.startswith('[pos')]
    P=Counter(); H6=Counter(); H1=Counter()
    for l in ms:
        mv=[int(x) for x in re.search(r'moves: ([\d,]+)',l).group(1).split(',')]
        P[min(len(mv)//5,8)]+=1
        H6[mv.count(6)]+=1; H1[mv.count(1)]+=1
    print(f.split('/')[-1],'ply/5',sorted(P.items()),'h6',sorted(H6.items()),'h1',sorted(H1.items()))
