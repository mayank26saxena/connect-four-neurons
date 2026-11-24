def vert2(b):
    g = b.grid
    for r0 in (0, 1):
        if all(g[r0 + k][2] == 2 for k in range(3)) and g[r0 + 3][2] == 0:
            return True
    return False

def diag(b):
    g = b.grid
    return g[2][2] == 2 and g[1][3] == 2 and g[0][4] != 1 and g[3][1] != 1

def box(b):
    g = b.grid
    return sum(1 for r in range(3) for c in (1, 2, 3) if g[r][c] == 2)

def fires(b):
    return vert2(b) or diag(b) or (b.grid[2][2] == 2 and box(b) >= 5)

def level(b):
    g = b.grid
    s = 0
    if vert2(b):
        s += 4
    if diag(b):
        s += 3
    if g[2][2] == 2:
        s += max(0, box(b) - 3)
    return min(9, s)
