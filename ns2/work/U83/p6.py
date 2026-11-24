def col3_ox(b):
    g = b.grid
    return b.heights[3] == 2 and g[0][3] == 2 and g[1][3] == 1

def fires(b):
    return col3_ox(b) and b.last_col != 3 and b.ply <= 21

def level(b):
    h = b.heights[3]
    if b.last_col == 3 or h > 2:
        return 0
    if fires(b):
        s = 6
        if b.ply <= 7:
            s += 2
        if b.last_row is not None and 2 <= b.last_row <= 3:
            s += 1
        return s
    if h >= 1 and b.grid[h - 1][3] == 1:
        return 3
    return 1
