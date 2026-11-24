import sys
from collections import Counter
def boards(fn):
    L=open(fn).read().split('\n'); out=[]
    for i,l in enumerate(L):
        if l.startswith('[pos'):
            out.append((l,L[i+1:i+7]))
    return out
D=[(0,1),(1,0),(1,1),(1,-1)]
def wins(g,p):
    s=set()
    for r in range(6):
        for c in range(7):
            if g[r][c]: continue
            for dr,dc in D:
                n=1
                for sg in (1,-1):
                    rr,cc=r+sg*dr,c+sg*dc
                    while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1; rr+=sg*dr; cc+=sg*dc
                if n>=4: s.add((r,c)); break
    return s
feat=sys.argv[1]
for bd in range(10):
    vals=[]
    for l,rows in boards(f'ns2/work/U88/ex_b{bd}.txt'):
        g=[[{'.':0,'X':1,'O':2}[ch] for ch in rows[5-r]] for r in range(6)]
        h=[sum(1 for r in range(6) if g[r][c]) for c in range(7)]
        mw=wins(g,1); tw=wins(g,2)
        vals.append(eval(feat))
    c=Counter(vals); print(bd,' '.join(f'{k}:{c[k]}' for k in sorted(c)))
