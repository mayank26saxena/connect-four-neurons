def fires(b):
    if b.ply < 1 or b.ply > 6:
        return False
    if b.last_col in (3, 4) and b.last_row == 0:
        return False
    return True

def level(b):
    if not fires(b):
        return 0
    return 6 if b.ply <= 4 else 4
