def count(b, c, who):
    return sum(1 for r in range(6) if b.grid[r][c] == who)

def core(b):
    c = b.last_col
    if c is None or b.ply >= 20:
        return 0
    if count(b, 1, 1) > 0:
        return 0
    col4 = count(b, 4, 1) + count(b, 4, 2)
    if col4 * 4 > b.ply:
        return 0
    if c == 1 and b.heights[1] <= 3:
        return 3 if b.heights[1] == 1 else 2
    if c == 0 and b.heights[0] <= 2 and b.ply <= 10:
        return 1
    if c == 2 and b.heights[2] == 1 and b.ply <= 8:
        return 1
    return 0

def fires(b):
    return core(b) > 0

def level(b):
    k = core(b)
    if k == 0:
        return 0
    base = {3: 7, 2: 5, 1: 4}[k]
    if b.ply <= 6:
        base += 1
    return min(9, base)
