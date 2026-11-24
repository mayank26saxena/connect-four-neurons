def fires(b):
    return b.grid[0][4] == 2 and b.grid[1][4] == 2

def level(b):
    return 6 if fires(b) else (2 if b.grid[0][4] == 2 else 0)
