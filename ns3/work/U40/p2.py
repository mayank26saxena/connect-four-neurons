def _s(b):
    g = b.grid
    if b.ply > 14:
        return -9
    s = 0.0
    for (r, c) in [(1, 2), (1, 3), (2, 2)]:
        if g[r][c] == 2:
            s += 1.0
    for (r, c) in [(0, 1), (0, 2), (0, 3)]:
        if g[r][c] == 2:
            s += 0.5
    if b.heights[4] >= 2:
        s -= 1.5
    if g[1][1] == 2 or g[1][4] == 2:
        s -= 1.0
    return s

def fires(b):
    return _s(b) >= 2.5

def level(b):
    s = _s(b)
    if s < 1.5:
        return 0
    return max(0, min(9, int((s - 1.5) * 3)))
