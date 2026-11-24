def _est(b):
    if b.last_col != 2:
        return None
    mine = sum(1 for r in range(6) if b.grid[r][2] == 1)
    theirs = sum(1 for r in range(6) if b.grid[r][2] == 2) - 1
    if mine == 0:
        return None
    p = b.ply
    if p <= 18:
        g = 2.6 - 0.3 * (18 - p)
    else:
        g = 2.6 - 0.06 * (p - 18)
    return g + 0.9 * (mine - 1) - 0.5 * theirs

def fires(b):
    e = _est(b)
    return e is not None and e >= 1.667

def level(b):
    e = _est(b)
    if e is None:
        return 0
    return int(max(0, min(9, round(e * 1.8))))
