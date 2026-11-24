def fires(b):
    if b.ply == 1:
        return b.last_col != 6
    return b.ply == 41

def level(b):
    if b.ply == 1:
        return {0: 7, 1: 4, 2: 4, 3: 4, 4: 6, 5: 9, 6: 2}[b.last_col]
    return 0
