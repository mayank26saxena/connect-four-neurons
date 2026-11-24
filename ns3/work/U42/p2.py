def _kind(b):
    # strongest reason the opponent can win at the landing cell of column 0
    r = b.landing(0)
    if r is None or (r, 0) not in b.their_playable_wins:
        return 0
    g = b.grid
    if r >= 3 and all(g[r - k][0] == 2 for k in (1, 2, 3)):
        return 2
    if r >= 3 and all(g[r - k][k] == 2 for k in (1, 2, 3)):
        return 1
    return 0

def fires(b):
    return _kind(b) > 0

def level(b):
    k = _kind(b)
    if k == 2:
        return 9 if b.last_col == 0 else 6
    if k == 1:
        return 6
    return 0
