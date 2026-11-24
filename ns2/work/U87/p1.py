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
    return 9 if b.last_col == 0 else 7
