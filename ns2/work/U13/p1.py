def fires(b):
    if b.ply == 6:
        return True
    return b.ply in (28, 30, 32) and b.last_col == 0

def level(b):
    if b.ply == 6:
        return 7
    if b.ply in (28, 30, 32) and b.last_col == 0:
        return 5
    return 0
