def mine_in(b, c):
    return sum(1 for r in range(6) if b.grid[r][c] == 1)

def score(b):
    c = b.last_col
    h = b.heights
    if c is None:
        return 0
    s = 0
    if c == 2:
        s = 3
        if h[3] == 0:
            s += 3
        elif h[3] == 1:
            s += 1
        if mine_in(b, 2) == 0:
            s += 1
        if b.ply <= 5:
            s += 2
        elif b.ply <= 8:
            s += 1
    elif c == 6:
        s = 2 + max(0, b.last_row - 1)
        if h[1] <= 4 and h[2] <= 4:
            s += 2
    elif c in (0, 1):
        s = 3
        if h[5] + h[6] <= 3:
            s += 3
    elif c == 4:
        s = 3
        if b.ply <= 6:
            s += 3
    return min(9, s)

def fires(b):
    return score(b) >= 7

def level(b):
    return score(b)
