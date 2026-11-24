def top2(b):
    h = b.heights[1]
    return h >= 2 and b.grid[h - 1][1] == 1 and b.grid[h - 2][1] == 1

def fires(b):
    return b.heights[0] <= 1 and b.heights[1] >= 3 and top2(b)

def level(b):
    h0 = b.heights[0]
    h1 = b.heights[1]
    if not top2(b):
        return 0
    v = h1 + 2 - 2 * h0 - b.heights[2] // 3 - b.ply // 12
    return max(0, min(9, v))
