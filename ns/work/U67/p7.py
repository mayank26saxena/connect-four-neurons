def parts(b):
    g, h = b.grid, b.heights
    a = h[1] == 0
    c2 = g[0][2] != 2
    right_low = min(h[4], h[5], h[6]) <= 1 and h[3] >= 2
    return a, c2, right_low

def fires(b):
    a, c2, rl = parts(b)
    return a and c2 and rl and b.ply >= 5

def level(b):
    a, c2, rl = parts(b)
    if not a:
        return 0
    s = 2 + (3 if c2 else 0) + (3 if rl else 0) + (1 if b.grid[0][2] == 1 else 0)
    return min(9, s)
