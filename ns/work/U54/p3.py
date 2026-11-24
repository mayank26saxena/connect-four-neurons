def c3(b, p):
    return sum(1 for k in range(6) if b.grid[k][3] == p)

def fires(b):
    return 2 <= b.ply <= 16 and c3(b, 2) > c3(b, 1)

def level(b):
    s = 0
    if b.ply <= 16:
        s += 3
    elif b.ply <= 24:
        s += 1
    s += max(-2, min(3, 2 * (c3(b, 2) - c3(b, 1))))
    if b.grid[0][3] == 2:
        s += 1
    return max(0, min(9, s + 2))
