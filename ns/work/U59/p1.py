def fires(b):
    return b.ply == 1 and b.last_col in (1, 2, 3, 4, 5)

def level(b):
    if not fires(b):
        return 0
    return 6 if b.last_col == 4 else 3
