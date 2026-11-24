def score_(b):
    s = 0.0
    lc = b.last_col
    if lc == 1 or lc == 6:
        s += 3
    elif lc == 4:
        s += 1
    h = b.heights
    if h[2] == 0:
        s += 1.5
    elif h[2] == 1:
        s += 0.5
    if h[0] <= 1:
        s += 1
    if 3 <= h[1] <= 5:
        s += 1.5
    if h[4] >= 5:
        s += 1
    for r in range(3):
        if b.grid[r][6] == 2:
            s += 0.5
    for r in range(2):
        if b.grid[r][5] == 2:
            s += 0.5
    if b.grid[0][0] == 1:
        s += 1
    if b.grid[1][3] == 1:
        s += 1
    return s

def fires(b):
    return score_(b) >= 8

def level(b):
    s = score_(b)
    return max(0, min(9, int(s - 2)))
