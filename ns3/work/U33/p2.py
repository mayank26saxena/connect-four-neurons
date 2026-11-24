def fires(b):
    return b.last_col == 5 and b.heights[5] == 1

def level(b):
    if b.last_col != 5:
        return 0
    h = b.heights[5]
    if h == 1:
        if b.ply <= 6:
            return 9
        return 7 if b.ply <= 14 else 5
    if all(b.grid[r][5] == 2 for r in range(h)):
        return 2
    return 0
