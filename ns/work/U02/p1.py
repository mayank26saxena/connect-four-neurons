def fires(b):
    return b.ply == 1 and b.last_col in (0, 3, 6)

def level(b):
    if b.ply == 1 and b.last_col == 3:
        return 9
    if b.ply == 1 and b.last_col in (0, 6):
        return 6
    return 0
