def _counts(b):
    mine = [0] * 7
    theirs = [0] * 7
    for r in range(6):
        for c in range(7):
            if b.grid[r][c] == 1:
                mine[c] += 1
            elif b.grid[r][c] == 2:
                theirs[c] += 1
    return mine, theirs

def _score(b):
    if b.last_col is None:
        return -9.0
    mine, theirs = _counts(b)
    nm = max(1, sum(mine))
    nt = max(1, sum(theirs))
    k = min(mine[4], theirs[1])
    s = k - 0.08 * (nm + nt) - 1.5 * theirs[5] / nt - 1.0 * theirs[6] / nt - 1.0 * mine[1] / nm
    if b.last_col in (1, 2, 4, 5):
        s += 0.3
    if b.me_first:
        s += 0.2
    return s

def fires(b):
    return _score(b) >= 1.2

def level(b):
    return max(0, min(9, int(round(_score(b) * 3))))
