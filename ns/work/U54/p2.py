def pts(b):
    g = b.grid
    s = 0.0
    if g[0][3] == 2:
        s += 1.5
    if g[0][3] == 1:
        s -= 1.0
    if g[0][6] == 2:
        s -= 1.0
    if g[0][5] == 2:
        s -= 1.0
    if g[0][1] == 2:
        s -= 0.5
    if 2 <= b.ply <= 16:
        s += 1.5
    elif b.ply > 24:
        s -= 1.5
    c, r = b.last_col, b.last_row
    if c is not None and r is not None and r >= 1 and g[r - 1][c] == 2:
        s += 1.0
    mine_c3 = sum(1 for k in range(6) if g[k][3] == 1)
    if mine_c3 == 0:
        s += 0.5
    return s

def fires(b):
    s = pts(b)
    v = 0.5 + (s - 3.5) / 8.0
    return max(0.0, min(1.0, v))

def level(b):
    return max(0, min(9, int(round(pts(b) * 1.5)) + 2))
