def fires(b):
    L = b.landing(3)
    return L is not None and L in (3, 4) and b.grid[L][2] == 2

def level(b):
    if not fires(b):
        return 0
    s = 4
    if b.landing(3) == 3:
        s += 2
    if b.grid[1][3] == 1:
        s += 1
    if b.grid[0][3] == 2:
        s += 1
    if b.grid[2][2] == 1:
        s += 1
    return min(s, 9)
