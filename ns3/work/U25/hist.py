import sys,re
rows={}
for line in open('ex.txt'):
    b=line.split()[0]; m=re.search(r'moves: ([0-9,]+)',line).group(1)
    mv=[int(x) for x in m.split(',')]
    if not (int(sys.argv[1])<=len(mv)<int(sys.argv[2])): continue
    h=[0]*7; g=[[0]*7 for _ in range(6)]
    for i,c in enumerate(mv):
        g[h[c]][c]=1+(i%2); h[c]+=1
    n=len(mv); me=1+(n%2)  # player to move: index n parity
    grid=[[0 if v==0 else (1 if v==me else 2) for v in r] for r in g]
    rows.setdefault(b,[]).append(grid)
grp={'lo':['B0','B1'],'hi':['B6','B7','B8','B9']}
for k,bs in grp.items():
    gs=[g for b in bs for g in rows[b]]
    print(k,len(gs))
    for r in range(5,-1,-1):
        print(' '.join('%2d/%2d/%2d'%tuple(round(100*sum(g[r][c]==v for g in gs)/len(gs)) for v in (0,1,2)) for c in range(7)))
