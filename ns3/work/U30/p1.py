def fires(b):
    if b.ply > 20:
        return False
    for (r, c) in [(1, 2), (2, 2), (1, 4), (2, 4)]:
        if b.grid[r][c] == 2:
            return False
    return True
