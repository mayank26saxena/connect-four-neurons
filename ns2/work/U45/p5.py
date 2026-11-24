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
    m = [x / nm for x in mine]
    t = [x / nt for x in theirs]
    core = 3.0 * min(m[4], t[1]) + 0.7 * m[4]
    pen = 1.5 * t[5] + 0.7 * t[6] + 0.5 * (m[1] + m[5] + m[6]) + 0.5 * t[4]
    lw = {0: -0.2, 1: 0.1, 2: 0.1, 3: 0.0, 4: 0.1, 5: 0.05, 6: -0.2}
    par = 0.1 if b.me_first else 0.0
    return core - pen + lw[b.last_col] + par

def fires(b):
    return _score(b) > 0.55

def level(b):
    s = _score(b)
    return max(0, min(9, int(round((s + 0.2) * 7))))
