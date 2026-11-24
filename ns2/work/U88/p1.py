def fires(b):
    if b.ply > 14:
        return False
    if any(h == 6 for h in b.heights):
        return False
    return len(b.my_wins) == 0

def level(b):
    if not fires(b):
        return 0
    return max(1, 9 - b.ply // 2)
