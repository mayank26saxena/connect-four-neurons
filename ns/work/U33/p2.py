def vstack(b, c):
    # number of opponent stones stacked at the top of column c
    h = b.heights[c]
    n = 0
    r = h - 1
    while r >= 0 and b.grid[r][c] == 2:
        n += 1
        r -= 1
    return n

def fires(b):
    for c in range(7):
        if b.heights[c] < 6 and vstack(b, c) >= 3 and c not in (4, 5):
            return True
    if b.grid[0][6] == 2 and b.grid[1][6] == 2 and b.heights[6] == 2:
        return True
    return False

def level(b):
    if not fires(b):
        return 0
    if b.heights[6] < 6 and vstack(b, 6) >= 3:
        return 9
    return 6
