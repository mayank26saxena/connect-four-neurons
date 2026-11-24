def fires(b):
    return b.heights[4] == 2 and b.heights[5] >= 2

def level(b):
    if b.heights[4] != 2:
        return 0
    s = 2
    if b.heights[5] >= 2:
        s += 3
    if b.grid[1][4] == 2:
        s += 2
    if b.last_col == 4:
        s += 2
    return min(s, 9)
