def _kind(b):
    r = b.landing(0)
    g = b.grid
    if r is not None and (r, 0) in b.their_playable_wins and r >= 3:
        if all(g[r - k][0] == 2 for k in (1, 2, 3)):
            return 9 if b.last_col == 0 else 7
        if all(g[r - k][k] == 2 for k in (1, 2, 3)):
            return 6
        if all(g[r][k] == 2 for k in (1, 2, 3)):
            return 6
    if b.their_playable_wins:
        return 2
    if r is not None and r >= 2 and b.last_col == 0 and g[r - 1][0] == 2 and g[r - 2][0] == 2:
        return 2
    if r is not None and (r, 0) in b.my_playable_wins:
        return 1
    return 0

def fires(b):
    return _kind(b) / 9.0

def level(b):
    return _kind(b)
