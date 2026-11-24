DIRS = ((0, 1), (1, 0), (1, 1), (1, -1))

def gain(b, p, r, c):
    # number of 4-windows through (r, c) that would hold >= 3 of p's stones and none of the other side's
    q = 3 - p
    n = 0
    for dr, dc in DIRS:
        for k in range(4):
            cells = [(r + (i - k) * dr, c + (i - k) * dc) for i in range(4)]
            if not all(0 <= rr < 6 and 0 <= cc < 7 for rr, cc in cells):
                continue
            vals = [b.grid[rr][cc] for rr, cc in cells if (rr, cc) != (r, c)]
            if q in vals:
                continue
            if vals.count(p) >= 2:
                n += 1
    return n

def fires(b):
    r = b.landing(4)
    if r is None:
        return False
    return gain(b, 2, r, 4) >= 2

def level(b):
    r = b.landing(4)
    if r is None:
        return 0
    return min(9, 3 * gain(b, 2, r, 4))
