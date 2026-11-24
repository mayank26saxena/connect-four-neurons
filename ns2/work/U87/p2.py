def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return vert3(b, 0) and b.heights[0] <= 4 and b.ply <= 34

def level(b):
    if not fires(b):
        return 0
    if b.ply <= 16:
        return 9
    if b.ply <= 24:
        return 8
    return 6
