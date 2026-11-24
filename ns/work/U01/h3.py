def base(b):
    return b.heights[3] == 4 and b.grid[3][3] == 2

def fires(b):
    if not base(b):
        return False
    return not (b.grid[2][3] == 1 and b.grid[1][3] == 1)

def level(b):
    if not base(b):
        return 0
    s = 4
    if b.grid[2][3] == 2:
        s += 3
        if b.grid[1][3] == 2:
            s += 1
    elif b.grid[1][3] == 1:
        s -= 2
    if b.last_col == 3:
        s += 1
    if b.ply > 20:
        s -= 1
    return max(1, min(9, s))
