def base(b):
    return b.heights[0] == 4 and b.grid[3][0] == 2

def fires(b):
    if not base(b):
        return False
    return b.last_col == 0 or (b.grid[2][0] == 1 and b.grid[1][0] == 1)

def level(b):
    if not base(b):
        return 0
    if b.grid[2][0] != 1:
        return 3 if b.last_col == 0 else 1
    lv = 5
    if b.grid[1][0] == 1:
        lv += 1
    if b.ply <= 14:
        lv += 2
    elif b.ply >= 30:
        lv -= 1
    if b.last_col == 0:
        lv += 1
    return min(lv, 9)
