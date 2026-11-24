CLUSTER = [(1, 2), (1, 3), (2, 1), (3, 1), (0, 2), (0, 3), (1, 1)]

def fires(b):
    g = b.grid
    if g[2][2] != 2 or g[0][4] == 1:
        return False
    if not (g[1][2] == 2 or g[1][3] == 2):
        return False
    return sum(1 for (r, c) in CLUSTER if g[r][c] == 2) >= 3

def level(b):
    g = b.grid
    n = sum(1 for (r, c) in CLUSTER if g[r][c] == 2)
    if g[2][2] != 2:
        return min(2, n // 3)
    s = n + (1 if g[0][4] != 1 else -2) + len([w for w in b.their_playable_wins])
    return max(0, min(9, s))
