import re,sys
def load(f):
    out=[]
    for l in open(f):
        mv=[int(x) for x in re.search(r'moves: ([\d,]*)',l).group(1).split(',') if x]
        a=float(re.search(r'act (-?[\d.]+)',l).group(1))
        out.append((mv,a))
    return out
def board(mv):
    g=[[0]*7 for _ in range(6)]; h=[0]*7; n=len(mv)
    for i,c in enumerate(mv):
        g[h[c]][c]=1 if (n-i)%2==0 else 2; h[c]+=1
    return g,h
D=[(0,1),(1,0),(1,1),(1,-1)]
def wins(g,p):
    s=set()
    for r in range(6):
        for c in range(7):
            if g[r][c]: continue
            for dr,dc in D:
                cnt=1
                for sg in (1,-1):
                    rr,cc=r+sg*dr,c+sg*dc
                    while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: cnt+=1; rr+=sg*dr; cc+=sg*dc
                if cnt>=4: s.add((r,c))
    return s
