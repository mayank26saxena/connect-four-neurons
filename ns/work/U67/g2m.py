# usage: g2m.py "row5/row4/.../row0" (top to bottom, X = player to move after sequence, O = other)
import sys
def win(g,p):
    R,C=6,7
    for r in range(R):
        for c in range(C):
            for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                if all(0<=r+k*dr<R and 0<=c+k*dc<C and g[r+k*dr][c+k*dc]==p for k in range(4)): return True
    return False
def solve(spec):
    rows=spec.split('/')[::-1]
    tgt=[[ch for ch in row] for row in rows]
    nx=sum(r.count('X') for r in tgt); no=sum(r.count('O') for r in tgt)
    # mover X: if nx==no, X moved first; if no==nx+1, O moved first
    if nx==no: first='X'
    elif no==nx+1: first='O'
    else: raise SystemExit('bad counts X=%d O=%d'%(nx,no))
    H=[sum(1 for r in range(6) if tgt[r][c]!='.') for c in range(7)]
    # build by removing from top (reverse): last move is by O... do forward DFS
    g=[['.']*7 for _ in range(6)]; h=[0]*7; seq=[]
    n=nx+no
    sys.setrecursionlimit(10000)
    def dfs(t):
        if t==n: return True
        p=first if t%2==0 else ('O' if first=='X' else 'X')
        for c in (3,2,4,1,5,0,6):
            if h[c]<H[c] and tgt[h[c]][c]==p:
                g[h[c]][c]=p; h[c]+=1; seq.append(c)
                if not win(g,p) and dfs(t+1): return True
                h[c]-=1; g[h[c]][c]='.'; seq.pop()
        return False
    if dfs(0): return ','.join(map(str,seq))
    raise SystemExit('no order')
print(solve(sys.argv[1]))
