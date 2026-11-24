# Hand-set template: (row, col): (weight if mine, weight if theirs). Split into a left half (cols 0-2),
# a right half (cols 4-6) and column 3; the unit needs BOTH halves plus a row-2 anchor.
LEFT = {
    (0, 0): (-0.75, -0.75), (0, 1): (1.0, 1.0), (0, 2): (0.75, 0.5),
    (1, 0): (-1.5, -1.5), (1, 1): (-1.5, -1.5), (1, 2): (0.0, 2.0),
    (2, 0): (-1.5, -1.5), (2, 1): (-1.5, -1.5), (2, 2): (1.5, -1.0),
    (3, 0): (-1.0, -1.0), (3, 1): (-1.0, -1.0), (3, 2): (0.5, 0.25),
}
RIGHT = {
    (0, 4): (0.0, 0.5), (0, 5): (-0.5, 1.25), (0, 6): (0.5, 0.25),
    (1, 4): (2.0, -1.0), (1, 5): (1.0, -1.0), (1, 6): (0.0, 0.25),
    (2, 4): (-1.5, 1.5), (2, 5): (-0.5, 0.5), (2, 6): (-0.25, -0.25),
    (3, 4): (0.25, 0.5),
}
MID = {
    (0, 3): (-0.25, -0.75), (1, 3): (-0.25, -0.25), (2, 3): (0.5, -0.75), (3, 3): (-1.0, 0.75),
}


def part(b, table):
    s = 0.0
    for (r, c), (wm, wt) in table.items():
        v = b.grid[r][c]
        if v == 1:
            s += wm
        elif v == 2:
            s += wt
    return s


def score(b):
    left = part(b, LEFT)
    right = part(b, RIGHT)
    high = sum(1 for r in (4, 5) for c in range(7) if b.grid[r][c] != 0)
    return left, right, left + right + part(b, MID) - 0.6 * high


def anchored(b):
    return b.grid[2][2] == 1 or b.grid[2][4] == 2


def fires(b):
    left, right, total = score(b)
    return anchored(b) and left >= 1.5 and right >= 2.5 and total >= 5.5


def level(b):
    left, right, total = score(b)
    if not anchored(b) or left < 0.5 or right < 1.5:
        return 0
    return max(0, min(9, int(total - 1.5)))
