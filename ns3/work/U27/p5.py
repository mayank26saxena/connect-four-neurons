def col2(b):
    h = b.heights[2]
    k = 0
    r = h - 1
    while r >= 0 and b.grid[r][2] == 1:
        k += 1
        r -= 1
    return k, h

def open_stack(b):
    k, h = col2(b)
    return k >= 2 and h < 6 and h - k + 4 <= 6

def my_col2_threat(b):
    return any(c == 2 for (r, c) in b.my_wins)

def fires(b):
    return open_stack(b) or my_col2_threat(b)

def level(b):
    k, h = col2(b)
    if open_stack(b) and k >= 3:
        return 9
    s = 0
    if my_col2_threat(b):
        s += 5
    if open_stack(b):
        s += 4
    return min(s, 9)
