def fires(b):
    if not b.me_first:
        return False
    n = (b.grid[0][0] == 2) + (b.grid[0][6] == 2)
    return n >= 1 and b.ply <= 12

def level(b):
    if not b.me_first:
        return 0
    n = (b.grid[0][0] == 2) + (b.grid[0][6] == 2) + (b.grid[0][1] == 2)
    if n == 0:
        return 0
    v = 3 * n
    if b.ply <= 8:
        v += 2
    return min(9, v)
