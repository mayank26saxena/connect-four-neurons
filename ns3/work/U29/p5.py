MINE = [(1, 2), (1, 3), (2, 1), (3, 2), (3, 3), (4, 4)]
THEIRS = [(2, 3), (4, 3), (3, 1), (3, 4), (1, 1)]

def cells(b):
    s = sum(1 for (r, c) in MINE if b.grid[r][c] == 1)
    s += sum(1 for (r, c) in THEIRS if b.grid[r][c] == 2)
    if b.heights[5] <= 1:
        s += 1
    return s

def poisoned(b):
    n = 0
    for c in b.legal:
        l = b.landing(c)
        if l < 5 and ((l + 1, c) in b.my_wins or (l + 1, c) in b.their_wins):
            n += 1
    return n

def score(b):
    if b.my_playable_wins or b.their_playable_wins:
        return 0
    return cells(b) + 2 * min(poisoned(b), 2)

def fires(b):
    return score(b) >= 9

def level(b):
    return max(0, min(9, score(b) - 3))
