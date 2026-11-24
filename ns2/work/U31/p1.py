def fires(b):
    return b.grid[0][2] == 2 and b.grid[1][2] == 0

def level(b):
    if not fires(b):
        return 0
    if b.last_col == 2:
        return 9 if b.ply <= 8 else 7
    return 5 if b.ply <= 12 else 3
