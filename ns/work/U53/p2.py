def fires(b):
    h = b.heights[2]
    if h == 2:
        if b.ply <= 7 or b.ply >= 26:
            return True
        return b.grid[0][2] == 1 and b.grid[1][2] == 2
    if h == 3:
        return b.ply >= 30
    return False

def level(b):
    h = b.heights[2]
    if h == 2:
        if b.ply <= 5:
            return 9
        if fires(b):
            return 6
        return 4
    if h == 3:
        return 4 if b.ply >= 30 else 2
    if h == 1:
        return 2
    return 0
