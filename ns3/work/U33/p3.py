def fires(b):
    if b.last_col != 5:
        return False
    h = b.heights[5]
    return h == 1 or (h == 2 and b.grid[0][5] == 2 and b.me_first)

def level(b):
    if b.last_col != 5:
        return 0
    h = b.heights[5]
    if h == 1:
        if b.ply <= 6:
            return 9
        return 7 if b.ply <= 14 else 5
    if all(b.grid[r][5] == 2 for r in range(h)):
        return 3 if (h == 2 and b.me_first) else 1
    return 0
