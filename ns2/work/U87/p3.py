def vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return vert3(b, 0)

def level(b):
    if not vert3(b, 0):
        return 0
    if b.ply <= 14:
        return 9
    if b.ply <= 22:
        return 8
    if b.ply <= 30:
        return 6
    return 4
