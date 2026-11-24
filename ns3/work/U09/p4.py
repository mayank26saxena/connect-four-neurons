def col2_three(b):
    h = b.heights[2]
    if h < 3 or h > 5:
        return 0
    t = b.grid[h - 1][2]
    if b.grid[h - 2][2] == t and b.grid[h - 3][2] == t:
        return t
    return 0

def col2_block(b):
    r = b.landing(2)
    if r is None:
        return False
    return (r, 2) in b.their_wins and b.last_col == 2

def fires(b):
    return col2_three(b) != 0 or col2_block(b)

def level(b):
    t = col2_three(b)
    if t == 2:
        return 9
    if t == 1:
        return 6
    if col2_block(b):
        return 3
    return 0
