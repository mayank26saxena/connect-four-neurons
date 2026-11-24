def _alt(b):
    a, m, c = b.grid[0][1], b.grid[0][2], b.grid[0][3]
    return a != 0 and m != 0 and a == c and a != m

def _s(b):
    if b.ply > 14 or not _alt(b):
        return 0
    g = b.grid
    s = 2
    s += sum(1 for (r, c) in [(1, 2), (1, 3), (2, 2)] if g[r][c] == 2)
    if g[0][0] == 2 or g[1][1] == 2:
        s -= 1
    if b.heights[4] > 1:
        s -= 1
    return s

def fires(b):
    return _s(b) >= 3

def level(b):
    return [0, 1, 2, 5, 7, 9, 9][max(0, _s(b))]
