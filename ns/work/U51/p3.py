def fires(b):
    return b.ply == 1 and b.last_col in (0, 1, 3, 6)

def level(b):
    if b.ply == 0:
        return 0
    if b.ply == 1:
        return {6: 9, 0: 8, 1: 7, 3: 6, 2: 3, 5: 3, 4: 3}[b.last_col]
    s = 1
    if b.last_row == 5:
        s += 1
    if b.last_col == 6:
        s += 1
    if b.last_col in (2, 5):
        s -= 1
    return s
