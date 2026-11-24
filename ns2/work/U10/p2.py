def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return any(vthree(b, c) for c in range(7))

def level(b):
    if vthree(b, 2):
        return 8
    if any(vthree(b, c) for c in range(7)):
        return 5
    return 0
