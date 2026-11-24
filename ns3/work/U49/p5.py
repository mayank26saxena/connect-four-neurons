def capped(b):
    n = 0
    for c in range(7):
        h = b.heights[c]
        if h >= 2 and b.grid[h - 1][c] == 2 and b.grid[h - 2][c] == 1:
            n += 1
    return n

def fires(b):
    return max(b.heights) <= 4 and b.ply <= 16 and capped(b) >= 2

def level(b):
    if max(b.heights) >= 6:
        return 0
    s = 5 - max(0, b.ply - 6) // 3 - max(0, max(b.heights) - 3) * 2 + 2 * capped(b)
    return max(0, min(9, s))
