def _s(b):
    g = b.grid
    h = b.heights
    if h[0] > 2 or h[1] < 2:
        return 0
    cells = [(3, 0), (2, 1), (1, 2), (0, 3)]
    if any(g[r][c] == 1 for r, c in cells):
        return 0
    n = sum(1 for r, c in cells if g[r][c] == 2)
    if n < 2 or g[1][2] != 2:
        return 0
    s = 2 + 2 * n
    if h[0] == 0:
        s += 1
    if g[1][1] == 1:
        s += 1
    return s

def fires(b):
    return _s(b) >= 6

def level(b):
    return min(9, _s(b))
