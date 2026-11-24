def col2(b):
    # (run, height): my unbroken run on top of column 2 and the column height
    h = b.heights[2]
    k = 0
    r = h - 1
    while r >= 0 and b.grid[r][2] == 1:
        k += 1
        r -= 1
    return k, h

def fires(b):
    k, h = col2(b)
    # at least two of mine on top, column not full, and a vertical four still fits
    return k >= 2 and h < 6 and h - k + 4 <= 6

def level(b):
    k, h = col2(b)
    if h >= 6:
        return 1
    if h - k + 4 > 6:
        return 0
    if k >= 3:
        return 9
    if k == 2:
        return 6 if h >= 3 else 4
    return 0
