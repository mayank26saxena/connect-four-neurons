def fires(b):
    h = b.heights[2]
    xo = b.grid[0][2] == 1 and b.grid[1][2] == 2
    if h == 2:
        if b.ply <= 7 or b.ply >= 28:
            return True
        return xo and b.ply <= 12
    if h == 3:
        return b.ply >= 31
    return False

def level(b):
    h = b.heights[2]
    if h == 2:
        if b.ply <= 5:
            return 9 if b.ply >= 3 else 6
        if b.ply <= 7:
            return 6
        if b.ply >= 28:
            return 5
        return 4 if b.ply <= 12 else 3
    if h == 3:
        return 4 if b.ply >= 31 else 2
    if h == 1:
        return 2
    return 0
