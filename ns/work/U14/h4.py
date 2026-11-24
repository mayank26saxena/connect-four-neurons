def fires(b):
    empty = [c for c in range(7) if b.heights[c] == 0]
    return b.ply >= 8 and len(empty) >= 1

def level(b):
    empty = [c for c in range(7) if b.heights[c] == 0]
    if not empty:
        return 0
    if b.ply >= 14:
        return 6
    if b.ply >= 8:
        return 4
    return 1
