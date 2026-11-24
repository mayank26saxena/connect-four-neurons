def toprun(b, c):
    n = 0
    r = b.heights[c] - 1
    while r >= 0 and b.grid[r][c] == 2:
        n += 1
        r -= 1
    return n

def fires(b):
    return b.ply <= 16 and b.heights[6] < 6 and toprun(b, 6) >= 2

def level(b):
    if b.ply > 20 or b.heights[6] >= 6:
        return 0
    n = toprun(b, 6)
    if n >= 3:
        return 9
    if n == 2:
        return 7 if b.ply <= 16 else 3
    return 1 if b.ply <= 12 else 0
