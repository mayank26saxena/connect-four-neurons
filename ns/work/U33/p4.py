def ocol6(b):
    n = 0
    for r in range(b.heights[6]):
        if b.grid[r][6] == 2:
            n += 1
        else:
            return -1
    return n

def fires(b):
    return b.heights[5] == 0 and ocol6(b) >= 1 and b.grid[0][3] == 1

def level(b):
    if b.heights[5] != 0 or ocol6(b) < 1:
        return 0
    s = 2 + 2 * ocol6(b)
    if b.grid[0][3] == 1:
        s += 2
    if b.grid[1][3] == 1:
        s += 1
    return min(9, s)
