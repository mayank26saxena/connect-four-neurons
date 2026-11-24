def fires(b):
    return b.grid[2][3] == 1 and b.grid[1][3] == 2

def level(b):
    s = 0
    if b.grid[2][3] == 1:
        s += 3
    if b.grid[1][3] == 2:
        s += 3
    return min(9, s)
