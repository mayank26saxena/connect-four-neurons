def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return vthree(b, 2) or vthree(b, 3)

def level(b):
    if vthree(b, 2):
        return 9
    if vthree(b, 3):
        return 6
    for c in (4, 5, 6):
        if vthree(b, c):
            return 3
    return 0
