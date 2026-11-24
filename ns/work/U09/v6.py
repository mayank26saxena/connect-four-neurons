THEIRS = {(2, 2): 2, (1, 3): 2, (1, 2): 1, (2, 1): 1, (3, 1): 1, (0, 1): 1, (0, 2): 1}
MINE = {(0, 0): 1, (0, 4): -2, (1, 3): -2, (2, 2): -2, (3, 1): -1}

def score(b):
    s = 0
    for (r, c), w in THEIRS.items():
        if b.grid[r][c] == 2:
            s += w
    for (r, c), w in MINE.items():
        if b.grid[r][c] == 1:
            s += w
    if b.last_col is not None and (b.last_row, b.last_col) in ((2, 1), (2, 2), (3, 1)):
        s += 2
    return s

def fires(b):
    return score(b) >= 6

def level(b):
    return max(0, min(9, 2 * (score(b) - 4)))
