def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h > 5:
        return 0
    t = b.grid[h - 1][c]
    if b.grid[h - 2][c] == t and b.grid[h - 3][c] == t:
        return t
    return 0

def col2_block(b):
    r = b.landing(2)
    if r is None:
        return False
    return (r, 2) in b.their_wins and b.last_col == 2

def left_fresh_three(b):
    c = b.last_col
    return c in (0, 1) and vthree(b, c) == 2

def fires(b):
    return vthree(b, 2) != 0 or col2_block(b) or left_fresh_three(b)

def level(b):
    t = vthree(b, 2)
    if t == 2:
        return 9
    if t == 1:
        return 6
    if col2_block(b) or left_fresh_three(b):
        return 3
    return 0
