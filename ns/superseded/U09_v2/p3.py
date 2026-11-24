def vert2(b):
    g = b.grid
    for r0 in (0, 1):
        if all(g[r0 + k][2] == 2 for k in range(3)) and g[r0 + 3][2] == 0:
            return True
    return False

def diag(b):
    g = b.grid
    return g[2][2] == 2 and g[1][3] == 2 and g[0][4] != 1 and g[3][1] != 1

def fires(b):
    return vert2(b) or diag(b)

def level(b):
    g = b.grid
    s = 0
    if vert2(b):
        s += 5
    if diag(b):
        s += 4
        if g[1][2] == 2:
            s += 1
        if g[2][1] == 2:
            s += 1
    return min(9, s)
