MINE = [-1.8, -4.8, -0.6, 0.0, -3.3, 0.9, -0.3]
THEIRS = [-5.7, -0.3, -2.4, -0.3, 0.0, 2.1, -1.0]
BASE = [0.45, 0.45, 0.45, 0.57, 0.76, 1.0, 0.53]

def score(b):
    if b.me_first or b.last_col is None:
        return -1.0
    if b.ply == 1:
        return [0.0, -0.4, 0.0, -0.3, 0.97, 1.65, 0.28][b.last_col]
    tot = 0.0
    for r in range(6):
        for c in range(7):
            v = b.grid[r][c]
            if v == 1:
                tot += MINE[c]
            elif v == 2 and not (r == b.last_row and c == b.last_col):
                tot += THEIRS[c]
    return BASE[b.last_col] + tot / (b.ply - 1)

def fires(b):
    return score(b) > 0.285

def level(b):
    s = score(b)
    if s <= 0.1:
        return 0
    return max(0, min(9, int((s - 0.1) / 0.18) + 1))
