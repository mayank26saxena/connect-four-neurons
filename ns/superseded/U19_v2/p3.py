def line_count(b, cells):
    n = 0
    for r, c in cells:
        if r < 0 or r > 5 or c < 0 or c > 6:
            return -1
        v = b.grid[r][c]
        if v == 1:
            return -1
        if v == 2:
            n += 1
    return n

def potential(b):
    # opponent's line potential through the cell (1,4)
    if b.grid[1][4] != 0:
        return 0.0
    rowbest = 0
    for s in (1, 2, 3):
        cells = [(1, s + k) for k in range(4) if s + k != 4]
        rowbest = max(rowbest, line_count(b, cells))
    d1 = max(0, line_count(b, [(0, 3), (2, 5), (3, 6)]))
    d2 = max(0, line_count(b, [(0, 5), (2, 3), (3, 2)]), line_count(b, [(2, 3), (3, 2), (4, 1)]))
    s = 2.0 * rowbest + 1.5 * d1 + 1.0 * d2
    if b.landing(4) == 1:
        s += 1.0
    return s

def fires(b):
    return potential(b) >= 3.0

def level(b):
    return max(0, min(9, int(round(potential(b) * 1.2 - 1))))
