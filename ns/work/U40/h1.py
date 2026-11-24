def fires(b):
    if b.ply != 3:
        return False
    for c in range(7):
        if b.grid[0][c] == 1:
            return c != 3
    return False
