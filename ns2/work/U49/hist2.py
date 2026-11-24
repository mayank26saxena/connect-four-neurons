import sys,re
lines=sys.stdin.read().split('\n')
recs=[]
for l in lines:
    m=re.match(r'\[pos \d+\] pole act ([-0-9.]+).*moves: ([0-9,]+)',l)
    if m: recs.append((float(m.group(1)),list(map(int,m.group(2).split(',')))))
def grid(mv):
    g=[[0]*7 for _ in range(6)]; h=[0]*7; n=len(mv)
    for i,c in enumerate(mv):
        g[h[c]][c]=1 if (i%2)==(n%2) else 2; h[c]+=1
    return g,h
D=[(1,0),(0,1),(1,1),(1,-1)]
def wins(g,p):
    s=set()
    for r in range(6):
        for c in range(7):
            if g[r][c]: continue
            for dr,dc in D:
                cnt=1
                for sgn in (1,-1):
                    rr,cc=r+sgn*dr,c+sgn*dc
                    while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: cnt+=1; rr+=sgn*dr; cc+=sgn*dc
                if cnt>=4: s.add((r,c))
    return s
def feats(mv):
    g,h=grid(mv); f={}
    f['ply']=len(mv)//4*4
    f['mywins']=min(3,len(wins(g,1))); f['theirwins']=min(3,len(wins(g,2)))
    for p,lab in ((1,'mycreate'),(2,'theircreate')):
        base=wins(g,p); k=0
        for c in range(7):
            if h[c]<6:
                g[h[c]][c]=p; w=wins(g,p)-base; g[h[c]][c]=0
                if w: k+=1
        f[lab]=min(4,k)
    lc=mv[-1]; f['lastcol']=lc; f['lastrow']=h[lc]-1
    f['nlegal']=sum(x<6 for x in h)
    return f
bands=[(-99,0.164),(0.164,0.459),(0.459,1.0),(1.0,99)]
from collections import Counter
FS=[(a,feats(m)) for a,m in recs]
for k in FS[0][1]:
    print('==',k)
    for lo,hi in bands:
        R=[f[k] for a,f in FS if lo<=a<hi]
        C=Counter(R); n=len(R)
        print(f'  {lo:>6}: n={n} '+' '.join(f'{v}:{C[v]*100//n}' for v in sorted(C)))
