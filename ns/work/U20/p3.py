def alive(g, r, c):
    # number of horizontal 4-windows containing (r,c),(r,c+1) with no opponent stone
    n = 0
    for s in range(max(0, c - 2), min(3, c) + 1):
        if all(g[r][s + k] != 2 for k in range(4)):
            n += 1
    return n

def score(b):
    if b.last_col is None:
        return 0
    lr, lc = b.last_row, b.last_col
    g = [row[:] for row in b.grid]
    best = 0
    for r in range(0, 3):
        for c in range(0, 6):
            if g[r][c] == 1 and g[r][c + 1] == 1 and r == lr and abs(lc - c) <= 3 and lc != c and lc != c + 1:
                g[lr][lc] = 0
                before = alive(g, r, c)
                g[lr][lc] = 2
                after = alive(g, r, c)
                if before > 0 and after == 0:
                    best = max(best, 2 if 1 <= c <= 2 else 1)
    return best

def fires(b):
    return score(b) >= 1

def level(b):
    return [0, 4, 8][score(b)]
