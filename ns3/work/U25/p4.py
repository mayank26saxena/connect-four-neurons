def early(b):
    g = b.grid
    if b.ply > 9 or g[0][3] != 2 or g[0][2] != 0:
        return False
    if not (g[0][1] == 1 or g[0][0] == 1 or g[0][4] == 1):
        return False
    if g[0][4] == 2 or g[0][5] == 2 or g[1][1] == 2:
        return False
    return True

def fires(b):
    return early(b)

def level(b):
    return 5 if early(b) else 0
