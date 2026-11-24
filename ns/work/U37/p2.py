def score(b):
    if b.heights[2] != 2 or b.grid[1][2] != 2:
        return None
    g = b.grid
    s = 0.0
    s += {0: 0, 1: 1, 2: -1}[g[1][1]]
    s += {0: 0, 1: 1, 2: -0.5}[g[1][3]]
    if g[2][1] == 2:
        s -= 1
    if g[2][3] == 2:
        s -= 1.5
    if g[0][2] == 1:
        s += 0.5
    if b.ply < 6:
        s -= 1
    return s

def fires(b):
    s = score(b)
    return s is not None and s >= 0.5

def level(b):
    s = score(b)
    if s is None:
        return 0
    return max(1, min(9, int(round(4 + 2 * s))))
