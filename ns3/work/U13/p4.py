def vert6(b):
    h = b.heights[6]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][6] == 2 for k in range(3))

def diag_threat6(b):
    r = b.landing(6)
    if r is None:
        return False
    for dr in (1, -1):
        ok = True
        for k in range(1, 4):
            rr = r - dr * k
            if rr < 0 or rr > 5 or b.grid[rr][6 - k] != 2:
                ok = False
        if ok:
            return True
    return False

def fires(b):
    if vert6(b):
        return True
    return diag_threat6(b) and b.last_col == 6

def level(b):
    if vert6(b):
        if b.my_playable_wins:
            return 5
        return 9 if b.last_col == 6 else 4
    if diag_threat6(b) and b.last_col == 6:
        return 3
    return 0
