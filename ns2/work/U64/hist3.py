import sys,re
for f in sys.argv[1:]:
    ms=[l for l in open(f) if l.startswith('[pos')]
    M=[[0]*7 for _ in range(6)];Tt=[[0]*7 for _ in range(6)];n=0
    for l in ms:
        mv=[int(x) for x in re.search(r'moves: ([\d,]+)',l).group(1).split(',')]
        h=[0]*7; me=len(mv)%2
        for i,c in enumerate(mv):
            if i%2==me: M[h[c]][c]+=1
            else: Tt[h[c]][c]+=1
            h[c]+=1
        n+=1
    print(f.split('/')[-1],'mine% / theirs% (top row first)')
    for r in range(5,-1,-1):
        print('  ',' '.join('%3d'%(100*M[r][c]//n) for c in range(7)),' | ',' '.join('%3d'%(100*Tt[r][c]//n) for c in range(7)))
