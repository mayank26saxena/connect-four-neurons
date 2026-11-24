def vert5(b):
    h = b.heights[5]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][5] == 2 for k in range(3))

def fires(b):
    return vert5(b)

def level(b):
    if vert5(b):
        return 8 if b.last_col == 5 else 5
    return 0
