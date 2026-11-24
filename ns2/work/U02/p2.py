def fires(b):
    return level(b) >= 5

def level(b):
    h = b.heights[3]
    g = b.grid
    if h == 0 or g[0][3] != 2:
        return 0
    if b.last_col == 3 and b.last_row == 0:
        return 9 if b.ply >= 12 else (7 if b.ply >= 8 else 5)
    if h == 1:
        return 5
    if h == 2 and g[1][3] == 2:
        return 5
    if h == 2:
        return 3
    return 1
