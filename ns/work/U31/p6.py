OPEN2 = {(0, 0), (0, 6), (1, 1), (3, 6), (4, 0), (4, 4), (4, 5), (4, 6), (5, 5), (5, 6), (6, 0), (6, 5), (6, 6)}

def strength(b):
    g = b.grid
    s = 0
    if g[3][5] == 2 and g[2][5] == 1:
        s = 6
        if g[1][5] == 1:
            s = 8
            if g[0][5] == 1:
                s = 9
    if g[3][3] == 2 and g[2][3] == 1 and g[1][3] == 1:
        s = max(s, 7)
    if s > 0:
        s -= 2 * sum(1 for r in range(6) if g[r][2] == 2)
        s -= 2 * len(b.my_wins)
        s -= len(b.their_wins)
        if b.ply > 18:
            s -= 2
        if b.ply > 26:
            s -= 2
    if b.ply == 2 and tuple(b.moves) in OPEN2:
        s = max(s, 6)
    if 2 < b.ply <= 6 and b.last_row is not None and b.last_row >= 1:
        if b.last_col in (0, 1, 4, 5) and g[b.last_row - 1][b.last_col] == 1:
            s = max(s, 6)
    return max(0, min(9, s))

def fires(b):
    return strength(b) >= 6

def level(b):
    return strength(b)
