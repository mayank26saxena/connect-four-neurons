import sys
for fn in sys.argv[1:]:
    tot=0; cnt={}
    for line in open(fn):
        mv=line.split('moves: ')[1].split('  ')[0].strip()
        moves=[int(x) for x in mv.split(',')] if mv else []
        n=len(moves); h=[0]*7; g=[[0]*7 for _ in range(6)]
        for i,c in enumerate(moves):
            g[h[c]][c]=i%2; h[c]+=1
        me=n%2
        if n<3: continue
        tot+=1
        for c in range(7):
            v=g[0][c] if h[c]>0 else None
            k=('X' if v==me else 'O') if v is not None else '.'
            cnt[(c,k)]=cnt.get((c,k),0)+1
    print(fn,tot)
    for c in range(7):
        print(c, {k:round(cnt.get((c,k),0)/tot,2) for k in 'XO.'})
