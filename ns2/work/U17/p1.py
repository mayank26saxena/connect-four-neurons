def fires(b):
    h = b.heights[1]
    if h < 3:
        return False
    return b.grid[h - 1][1] == 1

def level(b):
    h = b.heights[1]
    if h < 2 or b.grid[h - 1][1] != 1:
        return 0
    s = 0
    for r in range(h):
        if b.grid[r][1] == 1:
            s += 1
    v = h + s - 2
    if b.grid[h - 2][1] == 1:
        v += 1
    v -= b.heights[0] // 2 + b.heights[2] // 2
    return max(0, min(9, v))
