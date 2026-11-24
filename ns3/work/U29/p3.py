MINE = [(1, 2), (1, 3), (2, 1), (3, 2), (3, 3), (4, 4)]
THEIRS = [(2, 3), (4, 3), (3, 1), (3, 4), (1, 1)]

def score(b):
    s = sum(1 for (r, c) in MINE if b.grid[r][c] == 1)
    s += sum(1 for (r, c) in THEIRS if b.grid[r][c] == 2)
    if b.heights[5] <= 1:
        s += 1
    return s

def fires(b):
    return score(b) >= 8

def level(b):
    return max(0, min(9, 2 * (score(b) - 4)))
