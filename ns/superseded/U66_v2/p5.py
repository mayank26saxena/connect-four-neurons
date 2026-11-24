# template cells: (row, col) -> (colour expected, weight); 1 = mine, 2 = theirs
T = {
    (1, 6): (2, 2), (2, 6): (2, 2), (0, 6): (1, 1),
    (0, 4): (2, 1), (1, 4): (1, 1),
    (0, 3): (2, 1), (1, 3): (1, 1),
    (0, 2): (1, 1), (1, 2): (2, 1),
    (0, 0): (2, 1),
}

def pts(b):
    if b.last_col is None:
        return 0
    s = 0
    for (r, c), (v, w) in T.items():
        x = b.grid[r][c]
        if x == v:
            s += w
        elif x != 0:
            s -= w
    if b.grid[0][1] != 0:
        s -= 1
    if b.grid[0][5] != 0:
        s -= 0.5
    return s

def fires(b):
    return pts(b) >= 5

def level(b):
    return max(0, min(9, int(pts(b))))
