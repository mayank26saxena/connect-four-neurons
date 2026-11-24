W = [  # (row, col, who, weight)  who: 1 me, 2 them
    (2, 0, 2, 2.0), (2, 4, 1, 2.0), (1, 0, 2, 1.5), (0, 3, 2, 1.5), (1, 3, 1, 1.5),
    (1, 4, 2, 1.0), (3, 0, 1, 1.0), (3, 4, 2, 1.0), (0, 4, 1, 1.0), (0, 0, 2, 0.5),
    (0, 3, 1, -1.0), (1, 2, 2, -1.0), (2, 4, 2, -1.0), (0, 6, 2, -0.5),
]

def score(b):
    s = 0.0
    for r, c, w, x in W:
        if b.grid[r][c] == w:
            s += x
    return s

def fires(b):
    return score(b) >= 6.0

def level(b):
    s = score(b)
    return max(0, min(9, int(s * 1.2) - 1))
