def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return vthree(b, 1) or (vthree(b, 5) and b.heights[5] >= 4)

def level(b):
    if vthree(b, 1):
        return 9
    if vthree(b, 5):
        return 4 if b.heights[5] >= 4 else 1
    return 0
