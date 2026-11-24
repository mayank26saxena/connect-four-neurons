def toprun(b, c):
    h = b.heights[c]
    k = 0
    r = h - 1
    while r >= 0 and b.grid[r][c] == 2:
        k += 1
        r -= 1
    return k, r + 1, h - 1

def fires(b):
    return level(b) >= 3

def level(b):
    if b.heights[3] >= 6:
        return 0
    k, lo, hi = toprun(b, 3)
    if k >= 3 and lo >= 1:
        return 9
    if k >= 3:
        return 2
    if k == 2 and lo <= 2 and hi >= 2:
        return 5
    if k == 2:
        return 1
    return 0
