def raw(b):
    g = b.grid
    s = 0.0
    if g[1][3] == 1:
        s += 4
    elif g[1][3] == 2:
        s -= 3
    if g[0][0] == 2:
        s += 2
    if g[0][6] == 2:
        s += 1.5
    if g[0][3] == 1:
        s += 1
    if b.me_first:
        s += 0.5
    return s

def fires(b):
    return b.grid[1][3] == 1

def level(b):
    return max(0, min(9, int(raw(b))))
