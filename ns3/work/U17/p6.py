def motif(b):
    g = b.grid
    return (int(g[0][1] == 2) + int(g[0][2] == 1) + int(g[0][4] == 1)
            + int(g[0][5] == 2) + int(g[0][3] == 0))

def xhigh(b):
    return sum(1 for r in range(1, 6) for c in range(7) if b.grid[r][c] == 1)

def fires(b):
    if b.ply < 5 or b.ply > 11 or b.my_playable_wins:
        return False
    x = xhigh(b)
    m = motif(b)
    return (x == 0 and m >= 2) or (x == 1 and m >= 4)

def level(b):
    if b.ply < 5 or b.ply > 11 or b.my_playable_wins:
        return 0
    x = xhigh(b)
    m = motif(b)
    v = 2 * m - 3 * x
    return max(0, min(9, v))
