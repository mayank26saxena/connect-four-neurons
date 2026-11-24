def base(b):
    return b.heights[0] == 4 and b.grid[3][0] == 2

def fires(b):
    if not base(b):
        return False
    if b.last_col == 0:
        return b.grid[2][0] == 1 or b.ply <= 24
    return b.grid[2][0] == 1 and b.grid[1][0] == 1 and b.ply <= 20

def level(b):
    if b.heights[0] < 4 or b.grid[3][0] != 2:
        return 0
    if b.heights[0] > 4:
        return 2
    s = 2
    if b.last_col == 0:
        s += 3
    s += (b.grid[2][0] == 1) + (b.grid[1][0] == 1)
    if b.ply <= 12:
        s += 2
    elif b.ply <= 22:
        s += 1
    elif b.ply >= 32:
        s -= 1
    return max(1, min(s, 9))
