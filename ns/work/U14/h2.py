def top(b, c):
    h = b.heights[c]
    return b.grid[h - 1][c] if h > 0 else 0

def fires(b):
    return top(b, 4) == 1 and 2 <= b.heights[4] <= 5 and b.ply <= 26

def level(b):
    if top(b, 4) != 1:
        return 0
    h = b.heights[4]
    if h == 4:
        return 6
    if h in (3, 5):
        return 3
    return 1
