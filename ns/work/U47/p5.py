def fires(b):
    if b.heights[1] != 3:
        return False
    return b.grid[2][1] == 2 or b.grid[1][1] == 2 and b.ply >= 16

def level(b):
    if b.heights[1] != 3:
        return 0
    v = 4
    if b.grid[2][1] == 2:
        v += 2
    if b.last_col == 1:
        v += 3
    return v
