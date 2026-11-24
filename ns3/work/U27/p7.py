def col2(b):
    h = b.heights[2]
    k = 0
    r = h - 1
    while r >= 0 and b.grid[r][2] == 1:
        k += 1
        r -= 1
    return k, h

def stack2(b):
    k, h = col2(b)
    return k >= 2 and h < 6 and h - k + 4 <= 6

def their_right_stack(b):
    # opponent just stacked a second/third stone vertically in column 5 or 6
    c = b.last_col
    if c is None or c < 5:
        return False
    r = b.last_row
    return r >= 1 and b.grid[r - 1][c] == 2 and b.heights[2] > 0

def fires(b):
    return stack2(b) or their_right_stack(b)

def level(b):
    k, h = col2(b)
    s = 0
    if stack2(b):
        s = 9 if k >= 3 else (6 if h >= 3 else 4)
    if their_right_stack(b):
        s = min(9, s + 3)
    return s
