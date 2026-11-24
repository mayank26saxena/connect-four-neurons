def fires(b):
    if b.heights[0] != 4 or b.grid[3][0] != 2:
        return False
    return b.last_col == 0 or (b.grid[2][0] == 1 and b.grid[1][0] == 1)

def level(b):
    if b.heights[0] < 4 or b.grid[3][0] != 2:
        return 0
    if b.heights[0] > 4:
        return 2
    lv = 3
    if b.last_col == 0:
        lv += 3
    lv += (b.grid[2][0] == 1) + (b.grid[1][0] == 1)
    if b.ply <= 14:
        lv += 1
    return min(lv, 9)
