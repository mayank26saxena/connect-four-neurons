# build a move sequence (X first) reaching target columns; cols given bottom-up strings of X/O; X = first player
import sys
cols=[s if s!='-' else '' for s in sys.argv[1].split('/')]
nX=sum(c.count('X') for c in cols); nO=sum(c.count('O') for c in cols)
def wins(g,p):
    for r in range(6):
        for c in range(7):
            for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                ok=True
                for k in range(4):
                    rr,cc=r+dr*k,c+dc*k
                    if not(0<=rr<6 and 0<=cc<7 and g.get((rr,cc))==p): ok=False;break
                if ok: return True
    return False
import functools, random
sys.setrecursionlimit(10000)
seen=set()
def dfs(h,seq,g):
    key=tuple(h)
    if key in seen: return None
    seen.add(key)
    if all(h[c]==len(cols[c]) for c in range(7)): return seq
    p='X' if len(seq)%2==0 else 'O'
    order=list(range(7))
    if len(sys.argv)>2: random.shuffle(order)
    for c in order:
        if h[c]<len(cols[c]) and cols[c][h[c]]==p:
            g[(h[c],c)]=p
            if not wins(g,p):
                h[c]+=1; r=dfs(h,seq+[c],g); h[c]-=1
                if r: return r
            del g[(h[c],c)]
    return None
import random
if len(sys.argv)>2: random.seed(int(sys.argv[2]))
r=dfs([0]*7,[],{})
print(','.join(map(str,r)) if r else 'NONE')
