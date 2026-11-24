# usage: python mk.py "col0,col1,...,col6"  each col bottom-up string of X (me, to move) / O (them)
import sys
cols = sys.argv[1].split(',')
assert len(cols) == 7
ORDER = [int(x) for x in sys.argv[2]] if len(sys.argv) > 2 else [3,2,4,1,5,0,6]
n = sum(len(c) for c in cols)
me_first = (n % 2 == 0)
# player symbol for P1/P2
p1 = 'X' if me_first else 'O'
p2 = 'O' if me_first else 'X'
def four(grid):
    for r in range(6):
        for c in range(7):
            v = grid.get((r, c))
            if not v: continue
            for dr, dc in ((0,1),(1,0),(1,1),(1,-1)):
                if all(grid.get((r+k*dr, c+k*dc)) == v for k in range(4)): return True
    return False
sys.setrecursionlimit(10000)
seen = set()
def dfs(h, seq, grid):
    if len(seq) == n: return seq
    key = tuple(h)
    if key in seen: return None
    sym = p1 if len(seq) % 2 == 0 else p2
    for c in ORDER:
        if h[c] < len(cols[c]) and cols[c][h[c]] == sym:
            grid[(h[c], c)] = sym
            if not four(grid):
                h[c] += 1
                r = dfs(h, seq+[c], grid)
                if r: return r
                h[c] -= 1
            del grid[(h[c], c)]
    seen.add(key)
    return None
r = dfs([0]*7, [], {})
print(','.join(map(str, r)) if r else 'IMPOSSIBLE')
