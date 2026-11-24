def pts(b):
    s = 0
    g = b.grid
    if g[0][3] == 2:
        s += 2
    if g[0][3] == 1:
        s -= 2
    if not any(g[r][3] == 1 for r in range(6)):
        s += 1
    if g[0][5] == 0:
        s += 1
    if b.ply <= 16:
        s += 1
    if b.ply >= 26:
        s -= 1
    if b.their_playable_wins:
        s += 1
    return s

def fires(b):
    return pts(b) >= 5

def level(b):
    return max(0, min(9, pts(b) + 2))
