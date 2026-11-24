def nb(b):
    # filled cells beside and diagonal to the empty landing cell (2,4)
    n = 0
    for c in (3, 5):
        for r in (1, 2, 3):
            if b.grid[r][c] != 0:
                n += 1
    return n

def fires(b):
    return b.heights[4] == 2 and nb(b) >= 3

def level(b):
    if b.heights[4] != 2:
        return 0
    n = nb(b)
    s = 1 + n
    if b.grid[1][4] == 2:
        s += 2
    if b.last_col == 4:
        s += 1
    return min(s, 9)
