def vert_three(b, c, who):
    h = b.heights[c]
    if h < 3 or h >= 6:
        return False
    return all(b.grid[h - 1 - k][c] == who for k in range(3))

def fires(b):
    return vert_three(b, 0, 2)

def level(b):
    if vert_three(b, 0, 2):
        return 9
    if vert_three(b, 0, 1):
        return 3
    return 0
