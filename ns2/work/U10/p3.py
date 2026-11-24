def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    if vthree(b, 2):
        return True
    return b.last_col == 2 and b.last_row is not None and b.last_row <= 2 and b.ply <= 16

def level(b):
    if vthree(b, 2):
        return 8
    if fires(b):
        return 5
    if b.last_col == 2:
        return 3
    return 0
