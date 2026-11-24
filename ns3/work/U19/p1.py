def vthree(b, c, who):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == who for k in range(3))

def fires(b):
    return vthree(b, 5, 2) or vthree(b, 5, 1)

def level(b):
    if vthree(b, 5, 2):
        return 9 if b.last_col == 5 else 6
    if vthree(b, 5, 1):
        return 2
    return 0
