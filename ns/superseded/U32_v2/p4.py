# signature cells (row, col, owner): 1 = me, 2 = opponent
SIG = [(1, 2, 2), (2, 2, 1), (1, 4, 1), (2, 4, 2), (1, 5, 1), (0, 5, 2), (0, 4, 2),
       (0, 2, 1), (3, 3, 2), (3, 4, 1), (0, 3, 1)]
BAD = [(2, 2, 2), (2, 4, 1), (1, 2, 1), (0, 0, 1)]

def score(b):
    g = b.grid
    if b.heights[0] > 1 or b.heights[1] > 1:
        return 0
    s = sum(g[r][c] == v for r, c, v in SIG) - sum(g[r][c] == v for r, c, v in BAD)
    if g[1][2] == 2 and g[2][2] == 1:
        s += 2
    if g[1][4] == 1 and g[2][4] == 2:
        s += 2
    if b.heights[2] >= 5:
        s -= 2
    return s

def fires(b):
    return score(b) >= 6

def level(b):
    return max(0, min(9, score(b) - 1))
