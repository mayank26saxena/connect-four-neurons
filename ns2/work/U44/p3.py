def fires(b):
    g = b.grid
    return g[2][4] == 2 and g[1][4] == 1 and (b.ply < 16 or b.last_col == 4)

def level(b):
    g = b.grid
    s = 0
    if g[2][4] == 2 and g[1][4] == 1:
        s = 4
        if b.last_col == 4:
            s += 3
        if b.ply < 12:
            s += 2
    return min(9, s)
