def fires(b):
    L = b.landing(3)
    return L is not None and L in (3, 4) and b.grid[L][2] != 0

def level(b):
    L = b.landing(3)
    if L is None or L not in (2, 3, 4):
        return 0
    s = 2
    if b.grid[L][2] != 0:
        s += 2
    if b.grid[L][2] == 2:
        s += 1
    if L == 3:
        s += 2
    if b.grid[1][3] == 1:
        s += 1
    if b.grid[0][3] == 2:
        s += 1
    return min(s, 9)
