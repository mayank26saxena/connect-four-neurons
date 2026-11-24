def fires(b):
    if b.ply in (25, 27, 29, 31):
        return True
    if b.ply == 4 and b.last_col in (5, 6):
        return True
    return False

def level(b):
    if b.ply == 27:
        return 8
    if b.ply == 4 and b.last_col == 5:
        return 8
    if b.ply in (25, 29):
        return 5
    if b.ply == 31 or (b.ply == 4 and b.last_col == 6):
        return 4
    if b.ply in (23, 33, 16):
        return 2
    return 0
