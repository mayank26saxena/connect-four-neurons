def core(b):
    h = b.heights
    return h[0] == 0 and h[4] == 0 and h[1] > 0 and h[2] > 0 and h[3] > 0

def pair(b):
    g = b.grid
    return b.heights[0] == 0 and g[0][1] == 2 and g[0][2] == 1 and b.ply <= 10

def fires(b):
    if core(b):
        return b.ply <= 16 or b.grid[0][1] == 2
    return pair(b)

def level(b):
    s = 0
    if core(b):
        s += 5
    if pair(b):
        s += 3
    if s and b.ply <= 10:
        s += 1
    return min(9, s) if fires(b) else min(3, s)
