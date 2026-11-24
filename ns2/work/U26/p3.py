def top(b, c):
    h = b.heights[c]
    return (b.grid[h - 1][c], h) if h else (0, 0)

def score(b):
    s = 0
    o2, h2 = top(b, 2)
    if o2 == 2 and h2 in (1, 3):
        s += 2
    if b.grid[0][6] == 2 or b.grid[1][6] == 2:
        s += 1
    if b.heights[0] <= 2:
        s += 1
    if b.heights[1] <= 2:
        s += 1
    if b.heights[4] == 0:
        s += 1
    if b.heights[6] <= 2:
        s += 1
    if b.ply > 20:
        s -= 3
    return s

def fires(b):
    return score(b) >= 6

def level(b):
    return max(0, min(9, (score(b) - 2) * 2))
