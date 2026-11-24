def left_clear(b):
    g = b.grid
    return g[0][1] == 0 and g[0][2] != 2

def fires(b):
    if b.ply < 3 or not left_clear(b):
        return False
    if b.ply < 24:
        return not b.me_first
    return b.me_first

def level(b):
    if b.ply < 3 or not left_clear(b):
        return 0
    s = 3
    if (b.ply < 24) != b.me_first:
        s += 3
    if b.grid[0][2] == 1:
        s += 1
    s += min(2, sum(1 for r in range(6) if b.grid[r][3] == 2))
    return min(9, s)
