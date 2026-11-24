def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def fires(b):
    return vthree(b, 0) and b.heights[1] <= 3

def level(b):
    if not vthree(b, 0):
        return 0
    return max(1, 9 - 2 * b.heights[1])
