D1 = [(2, 0), (3, 1), (4, 2), (5, 3)]

def late(b):
    g = b.grid
    if g[4][2] != 2:
        return 0
    v = [g[r][c] for r, c in D1]
    if 1 in v:
        return 0
    return v.count(2)

def early(b):
    g = b.grid
    return b.ply <= 9 and g[0][1] == 1 and g[0][3] == 2 and g[0][2] == 0 and g[0][4] != 2

def fires(b):
    return late(b) >= 2 or early(b)

def level(b):
    d = late(b)
    if d >= 2:
        return min(9, 3 * d - 1)
    return 5 if early(b) else 0
