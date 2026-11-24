def vert1(b):
    h = b.heights[1]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][1] == 2 for k in range(3))

def fires(b):
    return vert1(b)

def level(b):
    return 9 if vert1(b) else 0
