ME_CELLS = {(1, 4): 2.0, (2, 2): 1.5, (1, 5): 1.0, (0, 2): 1.0, (2, 3): 0.75, (3, 4): 0.5}
THEM_CELLS = {(1, 2): 2.0, (2, 4): 1.5, (3, 3): 1.0, (0, 5): 0.75, (0, 4): 0.5, (2, 5): 0.5, (3, 2): 0.5}
WRONG_ME = {(1, 2): 1.0, (2, 4): 1.0, (3, 3): 1.0, (0, 5): 0.5}
WRONG_THEM = {(1, 4): 0.75, (2, 2): 1.0, (2, 3): 0.75, (1, 5): 0.5}


def score(b):
    g = b.grid
    s = 0.0
    for (r, c), w in ME_CELLS.items():
        if g[r][c] == 1:
            s += w
    for (r, c), w in THEM_CELLS.items():
        if g[r][c] == 2:
            s += w
    for (r, c), w in WRONG_ME.items():
        if g[r][c] == 1:
            s -= w
    for (r, c), w in WRONG_THEM.items():
        if g[r][c] == 2:
            s -= w
    # stones stacked in the two left columns suppress the unit
    s -= 1.0 * (max(0, b.heights[0] - 1) + max(0, b.heights[1] - 1))
    if b.heights[0] > 0:
        s -= 0.5
    return s


def fires(b):
    return score(b) >= 6.0


def level(b):
    s = score(b)
    if s < 2:
        return 0
    return min(9, int((s - 2) * 1.2))
