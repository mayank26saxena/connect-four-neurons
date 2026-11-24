import sys, re
from collections import Counter
def parse(fn):
    L=open(fn).read().split("\n"); out=[]
    for i,l in enumerate(L):
        if l.startswith("[pos"):
            a=float(re.search(r"pole act (-?[0-9.]+)",l).group(1))
            rows=L[i+1:i+7]
            g=[[".XO".index(rows[5-r][c]) for c in range(7)] for r in range(6)]
            out.append((a,g,l))
    return out
def wins(g,p):
    s=set()
    for r in range(6):
        for c in range(7):
            if g[r][c]: continue
            for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                n=1
                for sg in (1,-1):
                    rr,cc=r+sg*dr,c+sg*dc
                    while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1; rr+=sg*dr; cc+=sg*dc
                if n>=4: s.add((r,c)); break
    return s
def H(g): return [sum(1 for r in range(6) if g[r][c]) for c in range(7)]
def feats(g):
    h=H(g); tw=wins(g,2); mw=wins(g,1)
    f={}
    f["their_above_landing"]=[c for c in range(7) if h[c]<5 and (h[c]+1,c) in tw]
    f["my_above_landing"]=[c for c in range(7) if h[c]<5 and (h[c]+1,c) in mw]
    f["mustblock"]=[c for c in range(7) if h[c]<6 and (h[c],c) in tw]
    return f
fire=[x for x in parse(sys.argv[1]) if x[0]>0.349]
non=[x for x in parse(sys.argv[2]) if x[0]<=0.349]
for name in ("their_above_landing","my_above_landing","mustblock"):
    for grp,gn in ((fire,"fire"),(non,"non")):
        cs=[feats(x[1])[name] for x in grp]
        anyc=sum(1 for c in cs if c)/len(cs)
        print(name,gn,"%.2f"%anyc, sorted(Counter(c for cc in cs for c in cc).items()))
# coverage
cov=0
for x in fire:
    f=feats(x[1]); 
    if f["their_above_landing"] or 0 in f["mustblock"]: cov+=1
print("cover",cov/len(fire))
for x in fire:
    f=feats(x[1])
    if not (f["their_above_landing"] or 0 in f["mustblock"]): print(x[2][:110])
print("----")
def lastcell(l, g):
    c=int(re.search(r"last move col (\d)",l).group(1)) if "last move col" in l and re.search(r"last move col (\d)",l) else None
    if c is None: return None
    h=H(g)[c]; return (h-1,c)
def newthreat(x):
    a,g,l=x; lc=lastcell(l,g)
    if lc is None: return False
    tw=wins(g,2); g2=[row[:] for row in g]; g2[lc[0]][lc[1]]=0
    tw0=wins(g2,2)
    return len(tw-tw0)>0
def anythree(x):
    return len(wins(x[1],2))>0
for f,n in ((newthreat,"newthreat"),(anythree,"anythreat")):
    print(n, sum(map(f,fire))/len(fire), sum(map(f,non))/len(non))
