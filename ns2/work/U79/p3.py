def pure5(b):
    h = b.heights[5]
    return h >= 2 and h <= 3 and all(b.grid[r][5] == 2 for r in range(h))

def fires(b):
    if not pure5(b):
        return False
    return b.heights[5] == 3 or b.last_col == 5

def level(b):
    if not fires(b):
        return 0
    if b.heights[5] == 3:
        return 9
    return 5
