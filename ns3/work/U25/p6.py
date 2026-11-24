D1 = [(2, 0), (3, 1), (4, 2), (5, 3)]
D2 = [(2, 6), (3, 5), (4, 4), (5, 3)]

def dcount(b, cells):
    g = b.grid
    r, c = cells[2]
    if g[r][c] != 2:
        return 0
    v = [g[r][c] for r, c in cells]
    if 1 in v:
        return 0
    return v.count(2)

def late(b):
    if b.heights[3] >= 5:
        return 0
    return max(dcount(b, D1), dcount(b, D2))

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
