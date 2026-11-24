# template of the lower board (1 = mine, 2 = theirs) -> weight; matching colour +w, opposite colour -w/2
T = {
    (1, 6): (2, 2), (2, 6): (2, 2), (0, 6): (1, 1),
    (0, 4): (2, 1), (1, 4): (1, 1),
    (0, 3): (2, 1), (1, 3): (1, 1),
    (0, 2): (1, 1), (1, 2): (2, 1),
    (0, 0): (2, 1),
}

def pts(b):
    if b.last_col is None or b.ply < 3:
        return 0
    s = 0
    for (r, c), (v, w) in T.items():
        x = b.grid[r][c]
        if x == v:
            s += w
        elif x != 0:
            s -= w * 0.5
    if b.grid[0][1] == 0:
        s += 1
    if b.last_col in (0, 6):
        s += 1
    lc = b.last_col
    if lc in (3, 4) and b.last_row <= 2:
        s -= 1.5
    s -= max(0, b.ply - 18) * 0.15
    return s

def fires(b):
    v = (pts(b) - 1) / 10.0
    return max(0.0, min(1.0, v))

def level(b):
    return max(0, min(9, int(pts(b) - 1)))
