def fires(b):
    return b.heights[0] == 3 and b.grid[2][0] == 2

def level(b):
    if not fires(b):
        return 0
    n = sum(1 for r in range(3) if b.grid[r][0] == 2)
    lv = 3 + 2 * n
    if b.last_col == 0:
        lv += 1
    return min(lv, 9)
