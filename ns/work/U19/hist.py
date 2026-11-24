import sys
rows=[l.split() for l in open(sys.argv[1])]
data=[]
for r in rows:
    f = r[5]=="FIRES"
    s=r[r.index("moves:")+1]
    if s=="last": continue
    m=[int(x) for x in s.split(",")]
    g=[[0]*7 for _ in range(6)]; h=[0]*7
    for i,c in enumerate(m):
        g[h[c]][c]=i%2+1; h[c]+=1
    me = len(m)%2+1  # player to move: 1 if even plies
    G=[[0 if v==0 else (1 if v==me else 2) for v in row] for row in g]
    data.append((f,G))
for f in (True,False):
    sub=[G for ff,G in data if ff==f]
    print("FIRES" if f else "non", len(sub))
    for r in range(3,-1,-1):
        print(" ".join("%3d/%3d/%3d"%tuple(100*sum(G[r][c]==v for G in sub)//len(sub) for v in (0,1,2)) for c in range(7)))
