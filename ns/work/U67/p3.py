def fires(b):
    g = b.grid
    return b.ply >= 5 and g[0][1] == 0 and g[0][2] != 2 and b.heights[3] >= 2

def level(b):
    g = b.grid
    if g[0][1] != 0 or g[0][2] == 2:
        return 0
    s = 2 + sum(1 for r in range(6) if g[r][3] == 2) + (1 if g[0][2] == 1 else 0)
    return min(9, s)
