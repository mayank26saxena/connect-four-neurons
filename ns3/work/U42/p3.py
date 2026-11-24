def _kind(b):
    r = b.landing(0)
    if r is None:
        return 0
    g = b.grid
    if (r, 0) in b.their_playable_wins:
        if r >= 3 and all(g[r - k][0] == 2 for k in (1, 2, 3)):
            return 4
        if r >= 3 and all(g[r - k][k] == 2 for k in (1, 2, 3)):
            return 3
        if r >= 3 and all(g[r][k] == 2 for k in (1, 2, 3)):
            return 3
        return 0
    if (r, 0) in b.my_playable_wins and b.last_col == 0:
        return 2
    return 0

def fires(b):
    return _kind(b) > 0

def level(b):
    k = _kind(b)
    if k == 4:
        return 9 if b.last_col == 0 else 7
    if k == 3:
        return 6
    if k == 2:
        return 3
    return 0
