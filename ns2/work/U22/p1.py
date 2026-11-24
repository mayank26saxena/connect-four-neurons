def fires(b):
    return b.grid[3][3] == 2 and b.grid[2][4] == 2

def level(b):
    if not fires(b):
        return 0
    return 6
