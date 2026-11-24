def fires(b):
    return b.heights[5] == 6 and len(b.legal) <= 2

def level(b):
    if b.heights[5] != 6:
        return 0
    n = len(b.legal)
    base = {1: 8, 2: 6, 3: 4, 4: 2}.get(n, 0)
    if b.ply >= 34:
        base += 1
    return max(0, min(9, base))
