def _score(b):
    if b.last_col is None:
        return -9.0
    mine = [0] * 7
    theirs = [0] * 7
    for r in range(6):
        for c in range(7):
            if b.grid[r][c] == 1:
                mine[c] += 1
            elif b.grid[r][c] == 2:
                theirs[c] += 1
    nm = max(1, sum(mine))
    nt = max(1, sum(theirs))
    wm = [0.5, -1.0, 0.0, 0.0, 2.0, -1.0, -1.0]
    wt = [-0.5, 2.0, 0.0, 0.0, -0.5, -2.0, -1.0]
    s = sum(wm[c] * mine[c] / nm + wt[c] * theirs[c] / nt for c in range(7))
    lw = {0: -0.3, 1: 0.3, 2: 0.2, 3: 0.0, 4: 0.3, 5: 0.1, 6: -0.3}
    return s + lw[b.last_col]

def fires(b):
    return _score(b) > 0.75

def level(b):
    s = _score(b)
    return max(0, min(9, int(round((s + 0.25) * 6))))
