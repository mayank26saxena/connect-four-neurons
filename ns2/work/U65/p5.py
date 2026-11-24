def _caps(b):
    g = b.grid
    return (g[0][3] == 1 and g[1][3] == 2) + (g[0][5] == 1 and g[1][5] == 2)

def fires(b):
    g = b.grid
    if b.ply > 14:
        return False
    if any(g[r][6] == 1 for r in range(6)):
        return False
    return _caps(b) >= 1

def level(b):
    if not fires(b):
        return 0
    g = b.grid
    return min(9, 3 + 2 * _caps(b) + (g[2][3] == 1) + (g[3][3] == 2) + (b.ply <= 10))
