def fires(b):
    g = b.grid
    return g[0][6] == 2 and g[0][4] != 1 and g[0][5] != 1 and b.heights[6] <= 2

def level(b):
    if not fires(b):
        return 0
    g = b.grid
    k = 3 + 2 * sum(1 for c in (3, 4, 5) if g[0][c] == 2)
    if g[1][2] == 2:
        k += 2
    return min(9, k)
