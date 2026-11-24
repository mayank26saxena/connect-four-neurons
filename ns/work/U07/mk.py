# build a legal move sequence from columns given bottom-up as strings of 'F' (first player) / 'S' (second player)
# usage: python mk.py COL0 COL1 ... COL6   (use - for empty)
import sys
cols = [list(a) if a != '-' else [] for a in sys.argv[1:8]]
nf = sum(c.count('F') for c in cols); ns = sum(c.count('S') for c in cols)
assert nf - ns in (0, 1), (nf, ns)
# search: DFS over move orders that respect stacking and alternation
idx = [0]*7
seq = []
def dfs(turn):
    if len(seq) == nf + ns:
        return True
    for c in range(7):
        if idx[c] < len(cols[c]) and cols[c][idx[c]] == turn:
            idx[c] += 1; seq.append(c)
            if dfs('S' if turn == 'F' else 'F'):
                return True
            idx[c] -= 1; seq.pop()
    return False
print(','.join(map(str, seq)) if dfs('F') else 'IMPOSSIBLE')
