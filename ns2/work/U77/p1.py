def fires(b):
    if b.me_first:
        return False
    g = b.grid
    return g[0][0] == 1 and (g[0][6] == 2 or g[0][5] == 2)

def level(b):
    if not fires(b):
        return 0
    g = b.grid
    s = 4
    if g[0][6] == 2 and g[0][5] == 2:
        s += 3
    if g[0][4] == 2:
        s -= 3
    return max(1, min(9, s))
