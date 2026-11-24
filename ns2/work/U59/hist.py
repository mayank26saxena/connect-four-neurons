import sys,re
rows=[l for l in open('ex.txt')]
seen=set()
data={}
for l in rows:
    b=l.split()[0]; m=re.search(r'moves: (\S+)',l).group(1)
    if (b,m) in seen: continue
    seen.add((b,m))
    mv=[int(x) for x in m.split(',')]
    g=[[0]*7 for _ in range(6)]; h=[0]*7
    for i,c in enumerate(mv):
        g[h[c]][c]=i%2; h[c]+=1
    n=len(mv)
    # perspective: mover = player with index n%2 ; 'me' =1, them=2
    G=[[0 if r>=h[c] else (1 if g[r][c]==n%2 else 2) for c in range(7)] for r in range(6)]
    data.setdefault(b,[]).append((G,h))
for b in sorted(data):
    L=data[b]; N=len(L)
    print(b,N,'heights mean',[round(sum(x[1][c] for x in L)/N,1) for c in range(7)])
    for who,name in ((1,'me'),(2,'them')):
        print(' ',name)
        for r in range(3,-1,-1):
            print('   ',' '.join('%3d'%round(100*sum(x[0][r][c]==who for x in L)/N) for c in range(7)))
