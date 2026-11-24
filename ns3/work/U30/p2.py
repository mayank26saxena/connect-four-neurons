def vert3(b, p):
    for c in range(7):
        h = b.heights[c]
        if 3 <= h < 6 and all(b.grid[h - 1 - k][c] == p for k in range(3)):
            return True
    return False

def fires(b):
    return vert3(b, 2)
