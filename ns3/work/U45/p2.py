def fires(b):
    return level(b) >= 5

def level(b):
    if b.last_col is None:
        return 0
    c, r = b.last_col, b.last_row
    s = 0
    if c == 4 and r == 0:
        s = 9 if b.ply <= 5 else (6 if b.ply <= 9 else 3)
    elif c == 5 and r == 2:
        s = 6
    elif c == 5 and r == 3:
        s = 5
    elif (c, r) in ((0, 3), (1, 3), (3, 4), (2, 1)):
        s = 4
    if b.ply == 5:
        s = s + 3
    elif b.ply <= 9:
        s = s + 1
    elif b.ply >= 25:
        s = s - 2
    return max(0, min(9, s))
