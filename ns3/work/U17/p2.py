def raw(b):
    if b.ply < 5 or len(b.my_playable_wins) > 0 or len(b.their_playable_wins) > 0:
        return -9
    g = b.grid
    xhi = sum(1 for r in range(1, 6) for c in range(7) if g[r][c] == 1)
    ohi = sum(1 for r in range(1, 6) for c in range(7) if g[r][c] == 2)
    s = 0
    if g[0][1] == 2:
        s += 2
    if g[0][5] == 2:
        s += 1
    if g[0][1] == 2 and g[0][2] == 1:
        s += 1
    if g[0][5] == 2 and g[0][4] == 1:
        s += 1
    s += sum(1 for c in range(2, 6) if g[1][c] == 2)
    if ohi >= 1:
        s += 1
    s -= 3 * xhi
    return s

def fires(b):
    return raw(b) >= 3

def level(b):
    s = raw(b)
    if s < 1:
        return 0
    return min(9, 2 * s - 1)
