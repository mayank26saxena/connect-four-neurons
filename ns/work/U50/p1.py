def fires(b):
    if b.ply < 2 or b.ply > 8:
        return False
    if b.ply % 2 == 1:
        return False
    return b.last_col in (0, 3, 5, 6)

def level(b):
    if b.ply < 2 or b.ply > 10 or b.last_col is None:
        return 0
    w = {0: 4, 1: -6, 2: -2, 3: 4, 4: 2, 5: 2, 6: 4}[b.last_col]
    if b.ply % 2 == 1:
        w -= 3
    w += 4 - b.ply // 2
    return max(0, min(9, w))
