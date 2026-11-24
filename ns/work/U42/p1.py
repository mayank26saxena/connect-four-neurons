def _score(b):
    if b.last_col != 2:
        return None
    mine = sum(1 for r in range(6) if b.grid[r][2] == 1)
    theirs = sum(1 for r in range(6) if b.grid[r][2] == 2) - 1
    if mine == 0:
        return None
    return b.ply + 2 * mine - 3 * theirs

def fires(b):
    s = _score(b)
    return s is not None and s >= 18

def level(b):
    s = _score(b)
    if s is None:
        return 0
    return max(0, min(9, (s - 10) // 2))
