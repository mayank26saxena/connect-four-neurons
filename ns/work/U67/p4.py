def fires(b):
    g = b.grid
    return b.heights[1] == 0 and b.heights[2] <= 1 and g[0][2] != 2 and b.heights[3] >= 2

def level(b):
    g = b.grid
    if b.heights[1] != 0:
        return 0
    s = 3
    if g[0][2] == 2:
        s -= 2
    s -= max(0, b.heights[2] - 1)
    if b.heights[3] >= 2:
        s += 2
    s += sum(1 for r in range(1, 4) if g[r][3] == 2)
    return max(0, min(9, s))
