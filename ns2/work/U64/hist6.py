import sys,re
from collections import Counter
for f in sys.argv[1:]:
    ms=[l for l in open(f) if l.startswith('[pos')]
    C=Counter()
    for l in ms:
        mv=[int(x) for x in re.search(r'moves: ([\d,]+)',l).group(1).split(',')]
        col0=['1' if i%2==0 else '2' for i,c in enumerate(mv) if c==0]
        k=('odd' if len(mv)%2 else 'even')+':'+''.join(col0[:2])
        C[k]+=1
    print(f.split('/')[-1], sorted(C.items(), key=lambda x:-x[1])[:10])
