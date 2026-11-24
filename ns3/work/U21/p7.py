def mine_in(b, c):
    return sum(1 for r in range(6) if b.grid[r][c] == 1)

def level(b):
    L = b.last_col
    if L is None:
        return 0
    h = b.heights
    p = b.ply
    if L == 2:
        # opponent just played column 2: strongest early, with the centre column empty
        # and no stone of mine in column 2
        s = 3
        s += 3 if h[3] == 0 else (1 if h[3] == 1 else 0)
        s += 1 if mine_in(b, 2) == 0 else 0
        s += 2 if p <= 5 else (1 if p <= 8 else 0)
        return min(9, s)
    if L == 6:
        # opponent stacked column 6 high while columns 1-2 are not full
        s = 2 + max(0, b.last_row - 1)
        if h[1] <= 4 and h[2] <= 4:
            s += 2
        return min(8, s)
    if L in (0, 1):
        return 4 if p <= 20 else 3
    if L == 4:
        return 5 if p <= 6 else 3
    if L == 3:
        return 3 if p <= 16 else 2
    return 2

def fires(b):
    return level(b) >= 7
