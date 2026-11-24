def motif(b):
    g = b.grid
    if g[0][1] != 2:
        return 0
    s = 0
    if g[0][5] == 2:
        s += 2
    if g[0][4] == 2 and g[0][2] == 1:
        s += 2
    if g[0][2] == 1:
        s += 1
    if g[0][4] == 1:
        s += 1
    return s

def fires(b):
    if b.ply < 5 or b.my_playable_wins or b.their_playable_wins:
        return False
    xhi = sum(1 for r in range(1, 6) for c in range(7) if b.grid[r][c] == 1)
    return xhi == 0 and motif(b) >= 3

def level(b):
    if b.ply < 5 or b.my_playable_wins or b.their_playable_wins:
        return 0
    xhi = sum(1 for r in range(1, 6) for c in range(7) if b.grid[r][c] == 1)
    m = motif(b)
    if xhi == 0:
        return min(9, 2 * m + 1)
    if xhi == 1 and m >= 3:
        return 2
    return 0
