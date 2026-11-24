import sys
from collections import Counter
def board(m):
    g=[[0]*7 for _ in range(6)];h=[0]*7
    for i,c in enumerate(m):
        g[h[c]][c]=1+(i%2); h[c]+=1
    me=1+(len(m)%2)
    return g,h,me
def wins(g,p):
    s=set()
    for r in range(6):
        for c in range(7):
            if g[r][c]: continue
            for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                n=1
                for sgn in (1,-1):
                    rr,cc=r+sgn*dr,c+sgn*dc
                    while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1;rr+=sgn*dr;cc+=sgn*dc
                if n>=4: s.add((r,c))
    return s
mode=sys.argv[1]
cnt=Counter()
for l in sys.stdin:
    m=[int(x) for x in l.strip().split(',')]
    g,h,me=board(m); th=3-me
    tw=wins(g,th); mw=wins(g,me)
    land={c:h[c] for c in range(7) if h[c]<6}
    if mode=='poison':
        v=sum(1 for c,r in land.items() if (r+1,c) in tw)
    elif mode=='mb':
        v=sum(1 for c,r in land.items() if (r,c) in tw)
    elif mode=='anythreat':
        v=len(tw)
    cnt[v]+=1
print(sorted(cnt.items()))
