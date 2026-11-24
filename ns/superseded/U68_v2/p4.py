def vthree(b, c):
    h = b.heights[c]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][c] == 2 for k in range(3))

def col0_threats(b):
    return [r for (r, c) in b.their_wins if c == 0]

def fires(b):
    return vthree(b, 0) or len(col0_threats(b)) > 0

def level(b):
    if vthree(b, 0):
        return 9
    t = col0_threats(b)
    if t:
        return 5 if min(t) - b.heights[0] <= 1 else 3
    return 0
