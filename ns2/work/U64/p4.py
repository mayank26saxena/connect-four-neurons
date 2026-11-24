def fires(b):
    h0 = b.heights[0]
    if h0 < 1 or h0 > 2:
        return False
    if b.last_col == 0 or b.ply > 21:
        return False
    second = 2 if b.me_first else 1
    return all(b.grid[r][0] == second for r in range(h0))

def level(b):
    if not fires(b):
        return 0
    lvl = 4
    if not b.me_first and b.ply >= 13:
        lvl += 3
    return lvl
