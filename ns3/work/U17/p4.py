def core(b):
    g = b.grid
    left = g[0][1] == 2 and g[0][2] == 1 and g[0][4] != 0 and g[0][3] != 2
    right = g[0][5] == 2 and g[0][4] == 1 and (g[1][4] == 2 or g[1][3] == 2)
    return left, right

def xhigh(b):
    return sum(1 for r in range(1, 6) for c in range(7) if b.grid[r][c] == 1)

def fires(b):
    if b.ply < 5 or b.my_playable_wins:
        return False
    left, right = core(b)
    return (left or right) and xhigh(b) == 0

def level(b):
    if b.ply < 5 or b.my_playable_wins:
        return 0
    left, right = core(b)
    x = xhigh(b)
    if not (left or right):
        return 0
    if x == 0:
        return 9 if (left and right) else 7
    return 2 if x == 1 else 0
