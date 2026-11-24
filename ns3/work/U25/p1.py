def top2(b):
    h = b.heights[2]
    return b.grid[h-1][2] if h > 0 else 0

def fires(b):
    g = b.grid
    early = b.heights[2] == 0 and g[0][1] == 1 and g[0][3] == 2
    late = b.heights[2] >= 3 and (top2(b) == 2 or (b.heights[2] == 6 and g[4][2] == 2))
    return early or late

def level(b):
    return 6 if fires(b) else 0
