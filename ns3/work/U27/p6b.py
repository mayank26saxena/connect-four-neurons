def col2(b):
    h = b.heights[2]
    k = 0
    r = h - 1
    while r >= 0 and b.grid[r][2] == 1:
        k += 1
        r -= 1
    return k, h

def three_free(b):
    # my vertical three in column 2 with the cell above empty (immediate vertical win)
    k, h = col2(b)
    return k >= 3 and h < 6

def mid_pair(b):
    # my stones on rows 3 and 4 of column 2 (row index 2,3) with row 5 (index 4) still empty
    g = b.grid
    return g[2][2] == 1 and g[3][2] == 1 and g[4][2] == 0

def fires(b):
    return three_free(b) or mid_pair(b)

def level(b):
    if three_free(b):
        return 9
    if mid_pair(b):
        return 6
    k, h = col2(b)
    if k >= 2 and h < 6 and h - k + 4 <= 6:
        return 3
    g = b.grid
    if b.heights[2] == 6 and g[5][2] == 2 and g[4][2] == 1 and g[3][2] == 1:
        return 2
    return 0
