def score(b):
    g = b.grid
    s = 0.0
    if g[0][0] == 1: s += 2
    if g[0][1] == 2: s += 1
    if g[0][1] == 1: s -= 1.5
    if g[0][2] == 1: s += 0.5
    if g[0][5] == 2: s += 1
    if g[0][6] == 2: s += 1
    if g[0][4] == 1: s -= 1.5
    if g[0][4] == 2: s -= 1
    if g[1][0] == 2: s -= 0.7
    if g[1][1] == 1: s -= 1.5
    # dilution: stones above the bottom row
    up = b.ply - sum(1 for c in range(7) if g[0][c] != 0)
    s -= 0.25 * up
    return s

def fires(b):
    if b.me_first:
        return False
    return score(b) >= 3

def level(b):
    if b.me_first:
        return 0
    v = int(round((score(b) - 2) * 2.5))
    return max(0, min(9, v))
