def _est(b):
    if b.last_col != 2:
        return None
    mine = sum(1 for r in range(6) if b.grid[r][2] == 1)
    theirs = sum(1 for r in range(6) if b.grid[r][2] == 2) - 1
    p = b.ply
    if p <= 18:
        g = 2.6 - 0.3 * (18 - p)
    else:
        g = 2.6 - 0.1 * (p - 18)
    if mine == 0:
        bonus = -1.0
    else:
        bonus = 0.9 * (mine - 1)
    return g + bonus - 0.7 * theirs

def fires(b):
    e = _est(b)
    return e is not None and e >= 2.0

def level(b):
    e = _est(b)
    if e is None:
        return 0
    return int(max(0, min(9, round(e * 1.8))))
