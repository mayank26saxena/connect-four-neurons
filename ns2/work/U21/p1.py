def fires(b):
    empty = sum(1 for c in range(7) if b.heights[c] == 0)
    return b.ply <= 12 and empty >= 2

def level(b):
    empty = sum(1 for c in range(7) if b.heights[c] == 0)
    if b.ply > 16:
        return 0
    return max(0, min(9, empty + (16 - b.ply) // 3))
