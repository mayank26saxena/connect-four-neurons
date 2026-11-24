def col2(b):
    # my unbroken run on top of column 2 (k) and column height (h)
    h = b.heights[2]
    k = 0
    r = h - 1
    while r >= 0 and b.grid[r][2] == 1:
        k += 1
        r -= 1
    return k, h

def capped(b):
    # column 2 full, opponent stone on top, my two stones right under it
    g = b.grid
    return b.heights[2] == 6 and g[5][2] == 2 and g[4][2] == 1 and g[3][2] == 1

def open_stack(b):
    k, h = col2(b)
    return k >= 2 and h < 6 and h - k + 4 <= 6

def fires(b):
    return open_stack(b) or capped(b)

def level(b):
    k, h = col2(b)
    if open_stack(b):
        if k >= 3:
            return 9
        return 6 if h >= 3 else 4
    if capped(b):
        return 6 if b.grid[2][2] == 1 else 4
    return 0
