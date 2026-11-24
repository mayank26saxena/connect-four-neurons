W = [1.5, 0.8, 1.2, 0.5, 0.5, 0.0, 3.5]

def toprun(b, c):
    n = 0
    r = b.heights[c] - 1
    while r >= 0 and b.grid[r][c] == 2:
        n += 1
        r -= 1
    return n

def strength(b):
    s = 0.0
    for c in range(7):
        if b.heights[c] >= 6:
            continue
        n = toprun(b, c)
        if n >= 2:
            s = max(s, W[c] * (1.0 if n == 2 else 1.4))
    # fades in the late game
    if b.ply > 12:
        s -= 0.15 * (b.ply - 12)
    return s

def fires(b):
    return strength(b) >= 1.2

def level(b):
    s = strength(b)
    return max(0, min(9, int(round(s * 2))))
