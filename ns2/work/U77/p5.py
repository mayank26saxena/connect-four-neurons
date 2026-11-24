def est(b):
    g = b.grid
    s = 0.0
    if g[0][0] == 1: s += 2
    if g[0][0] == 2: s -= 0.8
    if g[0][1] == 2: s += 1
    if g[0][1] == 1: s -= 1.5
    if g[0][2] == 1: s += 0.5
    if g[0][4] == 1: s -= 1.5
    if g[0][4] == 2: s -= 1
    if g[0][5] == 2: s += 1.2
    if g[0][6] == 2: s += 1
    if g[1][0] == 2: s -= 0.7
    if g[1][1] == 1: s -= 2
    up = b.ply - sum(1 for c in range(7) if g[0][c] != 0)
    return s - 0.1 * up

def fires(b):
    if b.me_first:
        if b.ply == 4:
            return b.grid[0][1] == 1 and b.grid[0][6] != 2 and b.grid[0][0] != 2
        return False
    return est(b) >= 3.0

def level(b):
    if b.me_first:
        return 2 if fires(b) else 0
    v = int(round((est(b) - 2.0) * 2.5))
    return max(0, min(9, v))
