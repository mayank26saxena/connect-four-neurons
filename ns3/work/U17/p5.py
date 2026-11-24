def motif(b):
    g = b.grid
    return (int(g[0][1] == 2) + int(g[0][2] == 1) + int(g[0][4] == 1)
            + int(g[0][5] == 2) + int(g[0][3] == 0))

def xhigh(b):
    return sum(1 for r in range(1, 6) for c in range(7) if b.grid[r][c] == 1)

def fires(b):
    if b.ply < 5 or b.my_playable_wins:
        return False
    return motif(b) >= 4 and xhigh(b) <= 1

def level(b):
    if b.ply < 5 or b.my_playable_wins:
        return 0
    m = motif(b)
    x = xhigh(b)
    if m < 3:
        return 0
    v = 2 * m - 2 - 3 * x
    return max(0, min(9, v))
