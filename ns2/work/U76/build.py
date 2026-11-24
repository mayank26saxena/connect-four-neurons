import sys
# usage: build.py "rows top->bottom separated by /" mover(1|2)   X=mover's stones
rows = sys.argv[1].split('/')
mover = int(sys.argv[2])  # 1 = mover is first player
H = len(rows)
grid = [[rows[H-1-r][c] for c in range(7)] for r in range(H)]
cols = [[grid[r][c] for r in range(H) if grid[r][c] != '.'] for c in range(7)]
nx = sum(x.count('X') for x in cols); no = sum(x.count('O') for x in cols)
first = 'X' if mover == 1 else 'O'
second = 'O' if first == 'X' else 'X'
nf = nx if first == 'X' else no; ns = no if first == 'X' else nx
assert nf == ns + (0 if mover == 1 else 1) or nf == ns, (nf, ns)
total = nx + no
idx = [0]*7
seq = []
def dfs(t):
    if t == total: return True
    p = first if t % 2 == 0 else second
    for c in [3,2,4,1,5,0,6]:
        if idx[c] < len(cols[c]) and cols[c][idx[c]] == p:
            idx[c] += 1; seq.append(c)
            if dfs(t+1): return True
            idx[c] -= 1; seq.pop()
    return False
print(','.join(map(str, seq)) if dfs(0) else 'NONE')
