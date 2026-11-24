def col2(b):
    h = b.heights[2]
    k = 0
    r = h - 1
    while r >= 0 and b.grid[r][2] == 1:
        k += 1
        r -= 1
    return k, h

def capped(b):
    g = b.grid
    return b.heights[2] == 6 and g[5][2] == 2 and g[4][2] == 1 and g[3][2] == 1

def open_stack(b):
    k, h = col2(b)
    return k >= 2 and h < 6 and h - k + 4 <= 6

def right_last(b):
    return b.last_col is not None and b.last_col >= 4

def fires(b):
    k, h = col2(b)
    if open_stack(b) and k >= 3:
        return True
    return (open_stack(b) or capped(b)) and right_last(b)

def level(b):
    k, h = col2(b)
    s = 0
    if open_stack(b):
        s = 9 if k >= 3 else (5 if h >= 3 else 4)
    elif capped(b):
        s = 4
    if s and s < 9:
        s = s + 2 if right_last(b) else s - 2
    if s == 0 and right_last(b):
        s = 1
    return s
