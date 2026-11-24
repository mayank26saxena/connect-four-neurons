def _bottom(b):
    g = b.grid
    if g[0][1] != 0 or g[0][5] != 0:
        return 0
    a = g[0][2]
    if a == 0 or g[0][4] != a or g[0][3] not in (0, a):
        return 0
    return 1

def _late(b):
    h = b.heights
    if h[4] > 3:
        return 0
    full = sum(1 for c in (0, 1, 2, 5, 6) if h[c] >= 5)
    s = full
    t = set(b.their_wins) | set(b.my_wins)
    s += sum(1 for r in range(h[4], 6) if (r, 4) in t)
    return s

def _w(b):
    s = _late(b)
    if _bottom(b):
        s += 5
    if len(b.their_playable_wins) >= 2:
        s += 2
    return s

def fires(b):
    return _w(b) >= 5

def level(b):
    return min(9, _w(b))
