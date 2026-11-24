def opp_vert3(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return opp_vert3(b, 6)

def level(b):
    if opp_vert3(b, 6):
        return 8
    for c in range(6):
        if opp_vert3(b, c):
            return 2
    return 0
