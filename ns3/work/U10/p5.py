DIRS = ((0, 1), (1, 0), (1, 1), (1, -1))

def pot(b, p, r, c):
    # sum over 4-windows through empty cell (r, c) with no stone of the other side of (stones of p)^2
    q = 3 - p
    tot = 0
    for dr, dc in DIRS:
        for k in range(4):
            cells = [(r + (i - k) * dr, c + (i - k) * dc) for i in range(4)]
            if not all(0 <= rr < 6 and 0 <= cc < 7 for rr, cc in cells):
                continue
            vals = [b.grid[rr][cc] for rr, cc in cells]
            if q in vals:
                continue
            n = vals.count(p)
            tot += n * n
    return tot

def score(b):
    if b.grid[2][4] != 0:
        return 0
    return pot(b, 2, 2, 4)

def fires(b):
    return score(b) >= 8

def level(b):
    return min(9, score(b) // 2)
