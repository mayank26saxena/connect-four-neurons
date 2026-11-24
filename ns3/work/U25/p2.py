D1 = [(2, 0), (3, 1), (4, 2), (5, 3)]
D2 = [(2, 6), (3, 5), (4, 4), (5, 3)]

def diag(b, cells):
    v = [b.grid[r][c] for r, c in cells]
    if 1 in v:
        return 0
    return v.count(2)

def fires(b):
    return diag(b, D1) >= 2

def level(b):
    d = diag(b, D1)
    if d < 2:
        return 0
    return min(9, 3 * d - 2 + diag(b, D2))
