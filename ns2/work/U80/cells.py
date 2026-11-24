import sys,re
for f in sys.argv[1:]:
    txt=open(f).read()
    cnt={}; n=0
    for m in re.finditer(r'moves: ([\d,]+)',txt):
        mv=[int(x) for x in m.group(1).split(',')]; n+=1
        h=[0]*7; g={}
        for i,c in enumerate(mv):
            g[(h[c],c)]=i%2; h[c]+=1
        tomove=len(mv)%2
        for (r,c),p in g.items():
            k=(r,c,'M' if p==tomove else 'T'); cnt[k]=cnt.get(k,0)+1
    print(f,n)
    for r in range(5,-1,-1):
        print(' '.join('%2d/%2d'%(cnt.get((r,c,'M'),0)*100//n, cnt.get((r,c,'T'),0)*100//n) for c in range(7)))
