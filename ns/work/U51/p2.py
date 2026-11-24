def fires(b):
    if b.ply == 1:
        return b.last_col in (0, 1, 3, 6)
    return b.last_row == 5 and b.last_col in (0, 6)

def level(b):
    if b.ply == 1:
        return {6: 9, 0: 8, 1: 7, 3: 6, 2: 3, 5: 3, 4: 3}[b.last_col]
    if b.last_row == 5 and b.last_col in (0, 6):
        return 5
    return 0
