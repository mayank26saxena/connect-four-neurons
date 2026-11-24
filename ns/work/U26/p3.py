def fires(b):
    if b.ply % 2 == 1 or b.ply < 4 or b.ply > 14:
        return False
    g = b.grid
    if g[0][3] == 1:
        return False
    return g[0][4] == 2 or g[0][3] == 2

def level(b):
    return 6 if fires(b) else 0
