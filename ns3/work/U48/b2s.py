# helper: board picture (rows top->bottom, 'a'=first player, 'b'=second, '.'=empty) -> a legal move order
import sys
def solve(rows, last=None):
    rows=[r for r in rows]
    H=len(rows)
    cols=[[rows[H-1-r][c] for r in range(H) if rows[H-1-r][c]!='.'] for c in range(7)]
    n=sum(len(x) for x in cols)
    need_a=(n+1)//2
    if sum(x.count('a') for x in cols)!=need_a: return None
    if last is not None:
        lp='a' if (n-1)%2==0 else 'b'
        if not cols[last] or cols[last][-1]!=lp: return None
    idx=[0]*7; seq=[]
    sys.setrecursionlimit(10000)
    def dfs(k):
        if k==n: return True
        p='a' if k%2==0 else 'b'
        order=list(range(7))
        if last is not None and k==n-1: order=[last]
        for c in order:
            if last is not None and k<n-1 and c==last and idx[c]==len(cols[c])-1: continue
            if idx[c]<len(cols[c]) and cols[c][idx[c]]==p:
                idx[c]+=1; seq.append(c)
                if dfs(k+1): return True
                idx[c]-=1; seq.pop()
        return False
    return seq if dfs(0) else None
rows=sys.argv[1].split('/')
last=int(sys.argv[2]) if len(sys.argv)>2 else None
s=solve(rows,last)
print(','.join(map(str,s)) if s else 'NONE')
