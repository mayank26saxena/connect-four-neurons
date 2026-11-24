def raw(b):
    s = 0.0
    if b.heights[1] == 0:
        s += 2.0
    elif b.heights[1] == 1:
        s += 0.5
    if b.heights[0] <= 2:
        s += 0.5
    if b.me_first:
        s += 1.0
    # opponent stones low on the centre/right
    for (r, c) in ((0, 3), (0, 5), (1, 5), (0, 6), (1, 6), (1, 3)):
        if b.grid[r][c] == 2:
            s += 0.7
    # opponent stones in column 1 or my stones stacked in the centre hurt
    for r in range(6):
        if b.grid[r][1] == 2:
            s -= 1.0
    s -= b.ply / 12.0
    return s

def fires(b):
    return b.ply >= 2 and raw(b) >= 3.0

def level(b):
    if b.ply < 2:
        return 0
    v = int(round((raw(b) - 1.5) * 2))
    return max(0, min(9, v))
