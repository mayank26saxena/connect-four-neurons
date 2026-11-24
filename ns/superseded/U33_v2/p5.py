def toprun(b, c):
    n = 0
    r = b.heights[c] - 1
    while r >= 0 and b.grid[r][c] == 2:
        n += 1
        r -= 1
    return n

def strength(b):
    if b.ply < 3:
        return 0.0
    g = b.grid
    s = 0.0
    n6 = toprun(b, 6) if b.heights[6] < 6 else 0
    s += 2.0 * (n6 >= 2) + 1.0 * (n6 >= 3)
    s += 1.0 * (b.heights[1] == 0) + 1.0 * (b.heights[5] == 0)
    s += 1.0 * (g[0][6] == 2) + 0.7 * (g[0][2] == 2) + 0.7 * (g[0][3] == 1) - 1.0 * (g[0][3] == 2)
    s += 1.0 * any(b.heights[c] < 6 and toprun(b, c) >= 2 for c in (0, 2))
    if b.ply > 10:
        s -= 0.2 * (b.ply - 10)
    return s

def fires(b):
    return strength(b) >= 3.5

def level(b):
    s = strength(b)
    return max(0, min(9, int(round((s - 1.5) * 1.6))))
