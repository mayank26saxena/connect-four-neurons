def fires(b):
    if b.ply % 2 == 0:
        return b.ply >= 34
    return b.ply >= 39

def level(b):
    p = b.ply
    if p % 2 == 1:
        p = p - 3
    if p < 30:
        return 0
    return min(9, (p - 30) // 1)
