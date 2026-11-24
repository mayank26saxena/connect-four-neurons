def edge(b):
    return b.heights[0] + b.heights[6]

def fires(b):
    p = b.ply
    c = b.last_col
    if p == 1:
        return c == 1
    if p == 4 or p == 5:
        return c == 3
    if p >= 20 and p % 2 == 0:
        return edge(b) >= 9
    return False

def level(b):
    p = b.ply
    c = b.last_col
    if p == 4 and c == 3:
        return 9
    if p >= 20 and p % 2 == 0:
        e = edge(b)
        return max(0, min(9, e - 3))
    if fires(b):
        return 5
    return 0
