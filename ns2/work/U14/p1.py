def fires(b):
    return b.last_row == 2 and b.ply <= 12

def level(b):
    if b.last_row != 2:
        return 1 if b.ply <= 8 else 0
    if b.ply <= 8:
        return 7
    if b.ply <= 12:
        return 5
    return 2
