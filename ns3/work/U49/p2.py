def fires(b):
    if max(b.heights) > 4 or b.ply > 14:
        return False
    if b.last_row is None or b.last_row > 2:
        return False
    return len(b.their_wins) == 0 and len(b.my_wins) == 0

def level(b):
    if max(b.heights) >= 6:
        return 0
    s = 8 - max(0, b.ply - 6) // 2 - max(0, max(b.heights) - 3) * 2
    if b.last_row is not None and b.last_row > 2:
        s -= 2
    if fires(b):
        s += 1
    return max(0, min(9, s))
