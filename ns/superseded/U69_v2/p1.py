def fires(b):
    empty = 42 - b.ply
    return b.heights[1] == 6 and 4 <= empty <= 14

def level(b):
    if b.heights[1] != 6:
        return 0
    nfull = sum(1 for h in b.heights if h == 6)
    empty = 42 - b.ply
    if empty < 4:
        return 2
    return min(9, max(0, 2 * nfull - 2 - (2 if empty > 14 else 0)))
