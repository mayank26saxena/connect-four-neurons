def _bottom(b):
    g = b.grid
    if g[0][1] != 0 or g[0][5] != 0:
        return 0
    a = g[0][2]
    if a == 0 or g[0][4] != a:
        return 0
    if g[0][3] == a:
        return 3
    if g[0][3] == 0:
        return 2
    return 0

def _w(b):
    s = 2 * _bottom(b)
    if len(b.their_playable_wins) >= 2:
        s += 3
    elif len(b.their_playable_wins) == 1:
        s += 1
    return s

def fires(b):
    return _w(b) >= 3

def level(b):
    return min(9, _w(b) + 1 if _w(b) else 0)
