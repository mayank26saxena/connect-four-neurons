ME_CELLS = {(1, 4): 2.0, (2, 2): 2.0, (1, 5): 1.5, (0, 2): 0.5, (0, 6): 0.5, (0, 3): 0.5}
THEM_CELLS = {(1, 2): 1.5, (0, 5): 1.5, (2, 4): 1.5, (0, 4): 0.5, (0, 1): 1.0, (2, 5): 0.5}
WRONG_ME = {(1, 2): 1.5, (2, 4): 1.5, (0, 5): 1.0, (0, 1): 0.5}
WRONG_THEM = {(1, 4): 1.5, (2, 2): 1.0, (1, 5): 1.5, (0, 3): 0.5}
EMPTY_WANTED = {(1, 0): 1.0, (1, 1): 1.0, (2, 0): 1.0, (2, 1): 1.0, (0, 0): 0.5,
                (1, 3): 0.5, (2, 3): 0.5, (2, 6): 0.5, (3, 6): 0.5}


def score(b):
    s = 0.0
    for (r, c), w in ME_CELLS.items():
        if b.grid[r][c] == 1:
            s += w
    for (r, c), w in THEM_CELLS.items():
        if b.grid[r][c] == 2:
            s += w
    for (r, c), w in WRONG_ME.items():
        if b.grid[r][c] == 1:
            s -= w
    for (r, c), w in WRONG_THEM.items():
        if b.grid[r][c] == 2:
            s -= w
    for (r, c), w in EMPTY_WANTED.items():
        if b.grid[r][c] != 0:
            s -= w
    return s


def fires(b):
    return score(b) >= 7.0


def level(b):
    s = score(b)
    if s < 3:
        return 0
    return min(9, int(s - 2))
