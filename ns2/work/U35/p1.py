def fires(b):
    if b.last_col is None or b.last_col < 4 or b.last_row > 1:
        return False
    if b.ply > 14:
        return False
    right = sum(b.heights[c] for c in (4, 5, 6))
    return right * 2 >= b.ply

def level(b):
    if not fires(b):
        return 0
    return max(1, min(9, 10 - b.ply // 2))
