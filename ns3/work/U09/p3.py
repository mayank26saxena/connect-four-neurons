def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h > 5:
        return 0
    t = b.grid[h - 1][c]
    if b.grid[h - 2][c] == t and b.grid[h - 3][c] == t:
        return t
    return 0

def col2_threat(b):
    r = b.landing(2)
    if r is None:
        return False
    return (r, 2) in b.their_wins or (r, 2) in b.my_wins

def fires(b):
    return vthree(b, 2) != 0 or col2_threat(b) or vthree(b, 0) != 0 or vthree(b, 1) != 0

def level(b):
    t = vthree(b, 2)
    if t == 2:
        return 9
    if t == 1:
        return 6
    if col2_threat(b):
        return 3
    if vthree(b, 0) or vthree(b, 1):
        return 2
    return 0
