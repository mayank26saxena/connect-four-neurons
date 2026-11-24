def score_(b):
    g = b.grid
    s = 0
    s += 2 if g[0][3] == 1 else 0
    s += 2 if g[1][3] == 1 else 0
    s += 2 if g[2][3] == 2 else 0
    s += 1 if g[3][3] == 2 else 0
    s += 1 if b.heights[0] == 0 else 0
    s += 1 if b.heights[6] <= 1 else 0
    s += 1 if b.last_col == 3 else 0
    return s

def fires(b):
    return score_(b) >= 8

def level(b):
    return min(9, score_(b))
