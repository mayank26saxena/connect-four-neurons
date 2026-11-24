def base(b):
    return b.heights[3] == 4 and b.grid[3][3] == 2

def points(b):
    s = 0
    if b.grid[2][3] == 2:
        s += 2
    if b.last_col == 3:
        s += 2
    if b.grid[1][3] == 2:
        s += 1
    if b.ply <= 14:
        s += 1
    if b.ply >= 24:
        s -= 1
    if b.heights[4] <= 1:
        s += 1
    elif b.heights[4] >= 5:
        s -= 1
    return s

def fires(b):
    return base(b) and points(b) >= 3

def level(b):
    if not base(b):
        return 0
    return max(1, min(9, 1 + points(b)))
