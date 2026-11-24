def fires(b):
    return b.grid[1][5] == 2 and b.grid[2][5] == 0

def level(b):
    if not fires(b):
        return 0
    s = 4
    if b.grid[0][5] == 1:
        s += 2
    if b.grid[1][4] == 0:
        s += 2
    return min(s, 9)
