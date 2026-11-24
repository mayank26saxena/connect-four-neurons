def fires(b):
    h0 = b.heights[0]
    if h0 < 1 or h0 > 2:
        return False
    if b.last_col == 0:
        return False
    second = 2 if b.me_first else 1
    first = 3 - second
    if not all(b.grid[r][0] == second for r in range(h0)):
        return False
    return b.grid[0][1] == first

def level(b):
    if not fires(b):
        return 0
    lvl = 4
    if not b.me_first:
        lvl += 2
    if b.last_row is not None and b.last_row >= 4:
        lvl += 2
    return lvl
