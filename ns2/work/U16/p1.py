def fires(b):
    return b.heights[0] == 4 and b.grid[3][0] == 2 and b.grid[2][0] == 1

def level(b):
    if b.heights[0] != 4 or b.grid[3][0] != 2:
        return 0
    if b.grid[2][0] != 1:
        return 2
    lv = 5
    if b.grid[1][0] == 1:
        lv += 1
    if b.ply <= 14:
        lv += 2
    if b.last_col == 0:
        lv += 1
    return min(lv, 9)
