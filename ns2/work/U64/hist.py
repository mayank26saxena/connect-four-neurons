import sys,re
for f in sys.argv[1:]:
    ms=[l for l in open(f) if l.startswith('[pos')]
    H=[[0]*7 for _ in range(7)]; lc=[0]*7; odd=0; lr=[0]*6; n=0
    for l in ms:
        mv=[int(x) for x in re.search(r'moves: ([\d,]+)',l).group(1).split(',')]
        h=[0]*7
        for c in mv: h[c]+=1
        n+=1; odd+=len(mv)%2; lc[mv[-1]]+=1; lr[h[mv[-1]]-1]+=1
        for c in range(7): H[c][h[c]]+=1
    print(f.split('/')[-1], 'n',n,'oddply',odd,'lastcol',lc,'lastrow',lr)
    print('  mean heights',[round(sum(k*H[c][k] for k in range(7))/n,1) for c in range(7)])
    print('  col0 hist',H[0],'col1',H[1])
