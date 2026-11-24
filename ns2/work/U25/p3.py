def _pts(b):
    h = b.heights
    p = 0
    if h[3] == 6:
        p += 3
    elif h[3] == 0:
        p += 2
    if h[4] == 0:
        p += 2
    elif h[4] >= 5:
        p += 1
    if b.last_col == 4:
        p -= 3
    if b.last_col == 5:
        p += 1
    if b.ply <= 7:
        p += 2
    elif b.ply <= 16:
        p -= 3
    if h[5] >= 5:
        p -= 1
    theirs3 = sum(1 for r in range(6) if b.grid[r][3] == 2)
    if theirs3 >= 4:
        p += 1
    return p

def fires(b):
    return _pts(b) >= 5

def level(b):
    return max(0, min(9, _pts(b) + 2))
