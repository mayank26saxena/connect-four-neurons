def mine_in(b, c):
    return sum(1 for r in range(6) if b.grid[r][c] == 1)

def level(b):
    L = b.last_col
    if L is None:
        return 0
    p = b.ply
    h = b.heights
    if L == 2:
        v = 4
        if h[3] == 0:
            v += 3
        elif h[3] == 1:
            v += 1
        if mine_in(b, 2) == 0:
            v += 2
        else:
            v -= 1
        if p <= 6:
            v += 1
        elif p > 14:
            v -= 2
        return max(0, min(9, v))
    if L == 6:
        return 5 if h[6] >= 5 else (3 if h[6] >= 4 else 1)
    if L in (0, 1, 4):
        return 3 if p <= 20 else 2
    return 1

def fires(b):
    return level(b) >= 8
