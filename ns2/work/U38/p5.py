def run0(b):
    r = b.heights[0] - 1
    n = 0
    while r >= 0 and b.grid[r][0] == 2:
        n += 1
        r -= 1
    return n

def kind(b):
    if b.landing(0) is None:
        return 0
    n = run0(b)
    h = b.heights[0]
    if n >= 3:
        return 3
    if n == 2 and h == 4 and b.ply <= 22:
        return 2
    if n == 2 and h == 2 and b.last_col == 0:
        return 1
    return 0

def fires(b):
    return kind(b) > 0

def level(b):
    k = kind(b)
    if k == 3:
        return 9 if b.heights[0] >= 4 else 8
    if k == 2:
        return 3
    if k == 1:
        return 2
    return 0
