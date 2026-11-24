def edge(b):
    return b.heights[0] + b.heights[6]

def score(b):
    p = b.ply
    c = b.last_col
    if p == 0:
        return 0
    if p == 1:
        return 6 if c == 1 else 0
    s = 0
    if c == 3:
        s += 4
    if c == 0:
        s -= 4
    if p == 4 or p == 5:
        s += 3
    if p >= 20 and p % 2 == 0:
        s += 1 + edge(b) // 2
    if p >= 20 and p % 2 == 1:
        s -= 3
    s += b.heights[0] // 2
    return s

def fires(b):
    return score(b) >= 6

def level(b):
    return max(0, min(9, score(b) + 1))
