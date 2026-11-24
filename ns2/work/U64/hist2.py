import sys,re
for f in sys.argv[1:]:
    ms=[l for l in open(f) if l.startswith('[pos')]
    from collections import Counter
    C=Counter(); n=0
    for l in ms:
        mv=[int(x) for x in re.search(r'moves: ([\d,]+)',l).group(1).split(',')]
        col0=[ 'P1' if i%2==0 else 'P2' for i,c in enumerate(mv) if c==0]
        # who is me: ply even -> me P1
        me='P1' if len(mv)%2==0 else 'P2'
        s=''.join('m' if p==me else 't' for p in col0[:3])
        C[s]+=1; n+=1
    print(f.split('/')[-1], sorted(C.items(), key=lambda x:-x[1]))
