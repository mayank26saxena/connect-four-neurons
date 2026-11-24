import re,sys
for b in range(10):
    t=open(f"ns2/work/U20/band{b}.txt").read()
    ms=re.findall(r"moves: ([\d,]+)",t)
    H=[[0]*7 for _ in ms]; plies=[]
    for i,m in enumerate(ms):
        mv=[int(x) for x in m.split(",")]
        for c in mv: H[i][c]+=1
        plies.append(len(mv))
    n=len(ms)
    mean=[round(sum(h[c] for h in H)/n,1) for c in range(7)]
    full=[round(sum(h[c]==6 for h in H)/n,2) for c in range(7)]
    low=[round(sum(h[c]<=1 for h in H)/n,2) for c in range(7)]
    print(b,n,"ply",round(sum(plies)/n,1),"mean",mean,"\n   full",full,"\n   low<=1",low)
