def top_run(b, c):
    h = b.heights[c]
    n = 0
    r = h - 1
    while r >= 0 and b.grid[r][c] == 2:
        n += 1
        r -= 1
    return n

def level(b):
    h = b.heights[0]
    if h >= 6:
        return 0
    n = top_run(b, 0)
    if n >= 3:
        return 9
    if n == 2 and h == 4:
        return 4
    return 0

def fires(b):
    return level(b) >= 3
