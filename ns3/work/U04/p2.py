def top_run(b, c):
    h = b.heights[c]
    if h == 0:
        return 0, 0
    who = b.grid[h - 1][c]
    n = 0
    r = h - 1
    while r >= 0 and b.grid[r][c] == who:
        n += 1
        r -= 1
    return who, n

def level(b):
    h = b.heights[0]
    if h >= 6:
        return 0
    who, n = top_run(b, 0)
    if who == 2 and n >= 3:
        return 9
    if who == 2 and n == 2 and h <= 4:
        return 4
    if who == 1 and n >= 3:
        return 3
    return 0

def fires(b):
    return level(b) >= 3
