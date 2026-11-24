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
    m4 = mine[4] / nm
    t1 = theirs[1] / nt
    core = 4.0 * min(m4, t1)
    pen = (theirs[5] + 0.5 * theirs[6]) / nt + 0.5 * (mine[1] + mine[5] + mine[6]) / nm
    lw = {0: -0.2, 1: 0.1, 2: 0.1, 3: 0.0, 4: 0.1, 5: 0.0, 6: -0.2}
    par = 0.1 if b.me_first else 0.0
    return core - pen + lw[b.last_col] + par

def fires(b):
    return _score(b) > 0.6

def level(b):
    s = _score(b)
    return max(0, min(9, int(round((s + 0.2) * 7))))
