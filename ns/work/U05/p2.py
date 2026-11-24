def fires(b):
    if b.ply == 1:
        return b.last_col != 6
    if b.ply == 41:
        return True
    return b.last_col == 0 and 15 <= b.ply <= 22

def level(b):
    if b.ply == 1:
        return {0: 7, 1: 4, 2: 4, 3: 4, 4: 6, 5: 9, 6: 2}[b.last_col]
    if b.ply == 41:
        return 3
    if b.last_col == 0 and 15 <= b.ply <= 22:
        return 3
    return 0
